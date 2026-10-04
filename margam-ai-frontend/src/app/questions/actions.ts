"use server";

import { prisma } from "@/lib/db";
import { auth } from "@/lib/auth";
import { headers } from "next/headers";

export async function getSolvedQuestionIds() {
  const session = await auth.api.getSession({
    headers: await headers()
  });

  if (!session?.user) {
    return [];
  }

  const solved = await prisma.solvedQuestion.findMany({
    where: { userId: session.user.id },
    select: { questionId: true }
  });

  return solved.map(s => s.questionId);
}
