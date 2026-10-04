from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from pydantic import BaseModel
import jedi
import json
from app.api.v1.auth import verify_token

# Autocomplete router
router = APIRouter()

class AutocompleteRequest(BaseModel):
    id: str
    code: str
    line: int
    column: int

# Keep standard POST endpoint for backup (Temporarily unprotected)
@router.post("")
async def get_autocomplete(req: AutocompleteRequest):
    return process_jedi(req.dict())

@router.websocket("/ws")
async def autocomplete_ws(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            req = json.loads(data)
            
            result = process_jedi(req)
            await websocket.send_json(result)
                
    except WebSocketDisconnect:
        pass
    except Exception as e:
        print(f"WebSocket Error: {e}")

def process_jedi(req: dict) -> dict:
    try:
        code = req.get("code", "")
        line = req.get("line", 1)
        column = req.get("column", 0)
        req_id = req.get("id", "")
        
        script = jedi.Script(code)
        completions = script.complete(line, column)
        
        results = []
        for c in completions:
            results.append({
                "label": c.name,
                "kind": c.type,
                "detail": c.description,
                "insertText": c.name
            })
            
        return {"id": req_id, "suggestions": results}
    except Exception as e:
        print(f"Jedi autocomplete error: {e}")
        return {"id": req.get("id", ""), "suggestions": []}
