"use server";

import { prisma } from "@/lib/db";
import { auth } from "@/lib/auth";
import { headers } from "next/headers";
import { solutions } from "@/lib/curriculum/solutions";

export async function saveSubmission(params: {
  questionId: string;
  code: string;
  status: string;
  score: number;
}) {
  const session = await auth.api.getSession({
    headers: await headers()
  });

  if (!session?.user) {
    throw new Error("Unauthorized");
  }

  // 1. Create the submission record
  await prisma.submission.create({
    data: {
      userId: session.user.id,
      questionId: params.questionId,
      code: params.code,
      status: params.status,
      score: params.score,
    }
  });

  // 2. If SUCCESS, mark as solved
  if (params.status === "SUCCESS") {
    await prisma.solvedQuestion.upsert({
      where: {
        userId_questionId: {
          userId: session.user.id,
          questionId: params.questionId
        }
      },
      update: {}, // do nothing if it exists
      create: {
        userId: session.user.id,
        questionId: params.questionId
      }
    });
  }
  
  return { success: true };
}

export async function getMySubmissions(questionId: string) {
  const session = await auth.api.getSession({
    headers: await headers()
  });

  if (!session?.user) {
    return [];
  }

  return await prisma.submission.findMany({
    where: { 
      userId: session.user.id,
      questionId: questionId
    },
    orderBy: { createdAt: "desc" },
    select: {
      id: true,
      status: true,
      score: true,
      createdAt: true,
      code: true,
    }
  });
}

export async function getSolutionCode(questionId: string) {
  const session = await auth.api.getSession({
    headers: await headers()
  });

  if (!session?.user) {
    return "Unauthorized";
  }

  return solutions[questionId] || "Solution not available yet.";
}
