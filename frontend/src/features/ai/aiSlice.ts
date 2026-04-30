// features/ai/aiSlice.ts
import { createSlice, type PayloadAction } from "@reduxjs/toolkit";

interface AIState {
  input: string;
  loading: boolean;
}

const initialState: AIState = {
  input: "",
  loading: false,
};

const aiSlice = createSlice({
  name: "ai",
  initialState,
  reducers: {
    setInput: (state, action: PayloadAction<string>) => {
      state.input = action.payload;
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload;
    },
  },
});

export const { setInput, setLoading } = aiSlice.actions;
export default aiSlice.reducer;