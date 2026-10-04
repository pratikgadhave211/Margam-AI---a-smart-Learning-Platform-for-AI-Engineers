export interface QuestionMetadata {
  id: string; // e.g. "easy/question_1"
  title: string;
  difficulty: "Easy" | "Medium" | "Hard";
  topics: string[];
}

export const questionsList: QuestionMetadata[] = [
  {
    id: "easy/question_1",
    title: "1. The Support Bot — Structured JSON Output",
    difficulty: "Easy",
    topics: ["LangChain", "Structured Output", "Pydantic"],
  },
  {
    id: "easy/question_2",
    title: "2. The Conversationalist — Chat History",
    difficulty: "Easy",
    topics: ["LangChain", "Memory", "Messages"],
  },
  {
    id: "easy/question_3",
    title: "3. The Tokenizer — API Costs",
    difficulty: "Easy",
    topics: ["Tiktoken", "LLM Params", "Cost Control"],
  },
  {
    id: "easy/question_4",
    title: "4. The Few-Shot Learner — Tone & Persona",
    difficulty: "Easy",
    topics: ["FewShotPromptTemplate", "Examples", "Tone Control"],
  },
  {
    id: "easy/question_5",
    title: "5. The Streamer — Real-Time UX",
    difficulty: "Easy",
    topics: ["Streaming", "Async Generators", "UX"],
  }
];
