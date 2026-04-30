// app/store.ts
import { configureStore } from "@reduxjs/toolkit";
import formReducer from "../features/form/formSlice";
import aiReducer from "../features/ai/aiSlice";

export const store = configureStore({
  reducer: {
    form: formReducer,
    ai: aiReducer,
  },
});

// Types
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;