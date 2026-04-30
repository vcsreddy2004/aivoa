import { useState } from "react";
import { useAppSelector, useAppDispatch } from "../app/hooks";
import { setFormData } from "../features/form/formSlice";

export default function Form() {
    const form = useAppSelector((state) => state.form);
    const dispatch = useAppDispatch();
    const [prompt,setPrompt] = useState<string>("");
    const [messages, setMessages] = useState<{ text: string; sender: "user" | "ai" }[]>([]);
    const update = (field: string, value: any) => {
        dispatch(setFormData({ [field]: value }));
    };
    const handleAI = async () => {
        if (!prompt) return;

        setMessages((prev) => [...prev, { text: prompt, sender: "user" }]);
        const res = await fetch("http://localhost:8000/generate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: prompt}),
        });
        const data = await res.json();
        if (data.type === "history") {
            const historyMessages = data.data.map((item: any) => ({
                text: `${item.date} | ${item.interaction_type}
                    ${item.hcp_name || "No Name"}
                    ${item.topics || "No topics"}
                    ${item.outcomes || "No outcomes"}`,
                    sender: "ai" as const,
            }));
            setMessages((prev) => [...prev, ...historyMessages]);
        }
        else if(data.type === "followup") {
            setMessages((prev) => [...prev, { text: data.data, sender: "ai" as const }]);
        }
        else {
            setMessages((prev) => [
                ...prev,
                {
                    text: `Filled form`,
                    sender: "ai",
                },
            ]);
        }
        dispatch(setFormData(data));
    };
    return (
        <div className="flex gap-6 p-6 bg-gray-100 min-h-screen">
            {/* LEFT FORM */}
            <div className="w-2/3 bg-white p-6 rounded-xl shadow">
                <h2 className="text-lg font-semibold mb-4">Log HCP Interaction</h2>

                {/* HCP Name + Interaction Type */}
                <div className="grid grid-cols-2 gap-4 mb-4">
                <input
                    className="border p-2 rounded"
                    placeholder="HCP Name"
                    value={form.hcp_name}
                    onChange={(e) => update("hcp_name", e.target.value)}
                />

                <select
                    className="border p-2 rounded"
                    value={form.interaction_type}
                    onChange={(e) => update("interaction_type", e.target.value)}
                >
                    <option value="">Select Type</option>
                    <option value="Meeting">Meeting</option>
                    <option value="Call">Call</option>
                    <option value="Visit">Visit</option>
                </select>
                </div>

                {/* Date + Time */}
                <div className="grid grid-cols-2 gap-4 mb-4">
                <input
                    type="text"
                    className="border p-2 rounded"
                    value={form.date}
                    onChange={(e) => update("date", e.target.value)}
                />
                <input
                    type="time"
                    className="border p-2 rounded"
                    value={form.time}
                    onChange={(e) => update("time", e.target.value)}
                />
                </div>

                {/* Attendees */}
                <input
                className="border p-2 rounded w-full mb-4"
                placeholder="Attendees (comma separated)"
                value={form.attendees.join(", ")}
                onChange={(e) =>
                    update("attendees", e.target.value.split(","))
                }
                />

                {/* Topics */}
                <textarea
                className="border p-2 rounded w-full mb-4"
                placeholder="Topics Discussed"
                value={form.topics}
                onChange={(e) => update("topics", e.target.value)}
                />

                {/* Materials */}
                <input
                className="border p-2 rounded w-full mb-4"
                placeholder="Materials Shared"
                value={form.materials}
                onChange={(e) => update("materials", e.target.value)}
                />

                {/* Samples */}
                <input
                className="border p-2 rounded w-full mb-4"
                placeholder="Samples Distributed"
                value={form.samples}
                onChange={(e) => update("samples", e.target.value)}
                />

                {/* Sentiment */}
                <div className="mb-4">
                <p className="font-medium mb-2">HCP Sentiment</p>
                {["Positive", "Neutral", "Negative"].map((s) => (
                    <label key={s} className="mr-4">
                    <input
                        type="radio"
                        checked={form.sentiment === s}
                        onChange={() => update("sentiment", s)}
                    />{" "}
                    {s}
                    </label>
                ))}
                </div>

                {/* Outcomes */}
                <textarea
                className="border p-2 rounded w-full mb-4"
                placeholder="Outcomes"
                value={form.outcomes}
                onChange={(e) => update("outcomes", e.target.value)}
                />

                {/* Follow-up */}
                <textarea
                className="border p-2 rounded w-full"
                placeholder="Follow-up Actions"
                value={form.follow_up}
                onChange={(e) => update("follow_up", e.target.value)}
                />
            </div>

            {/* RIGHT AI CHAT PANEL */}
            <div className="w-1/3 bg-white p-4 rounded-xl shadow flex flex-col">
                <h3 className="font-semibold mb-3">AI Assistant</h3>

                <div className="flex-1 border rounded p-3 mb-3 overflow-y-auto flex flex-col gap-2 h-100">
                    {messages.map((msg, index) => (
                        <div
                        key={index}
                        className={`p-2 rounded max-w-[80%] ${
                            msg.sender === "user"
                            ? "bg-blue-500 text-white self-end"
                            : "bg-gray-200 self-start"
                        }`}
                        >
                        {msg.text}
                        </div>
                    ))}
                </div>

                <div className="flex gap-2">
                <input
                    onChange={(e)=>setPrompt(e.target.value)}
                    className="border p-2 rounded flex-1"
                    placeholder="Describe interaction..."
                />
                <button onClick={handleAI} className="bg-blue-500 text-white px-4 rounded">
                    Log
                </button>
                </div>
            </div>
        </div>
    );
}