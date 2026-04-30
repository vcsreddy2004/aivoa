// features/form/formSlice.ts
import { createSlice, type PayloadAction } from "@reduxjs/toolkit";
import type { FormState } from "./formTypes";

const initialState: FormState = {
  hcp_name: "",
  interaction_type: "",
  date: "",
  time: "",
  attendees: [],
  topics: "",
  materials: "",
  samples: "",
  sentiment: "Neutral",
  outcomes: "",
  follow_up: "",
};

const formSlice = createSlice({
  name: "form",
  initialState,
  reducers: {
    setFormData: (state, action: PayloadAction<Partial<FormState>>) => {
      return { ...state, ...action.payload };
    },
    resetForm: () => initialState,
  },
});

export const { setFormData, resetForm } = formSlice.actions;
export default formSlice.reducer;