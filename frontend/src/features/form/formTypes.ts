// features/form/formTypes.ts
export interface FormState {
  hcp_name: string;
  interaction_type: string;
  date: string;
  time: string;
  attendees: string[];
  topics: string;
  materials: string;
  samples: string;
  sentiment: "Positive" | "Neutral" | "Negative";
  outcomes: string;
  follow_up: string;
}