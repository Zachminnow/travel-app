import React from "react";
import {
  BarChart,
  Bar,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

const AboutChart = () => {
  const colors = [
    "#FF6384", // Pink
    "#4BC0C0", // Teal
    "#997790", // Purple
    "#FF9F40", // Orange
  ];

  const data = [
    { name: "Travel", value: 400 },
    { name: "Adventure", value: 300 },
    { name: "Relaxation", value: 300 },
    { name: "Culture", value: 200 },
  ];

  return (
    <div className="w-full h-[300px] flex items-center justify-center bg-white p-4 rounded-lg shadow-md">
      <ResponsiveContainer width="90%" height="100%">
        <BarChart data={data} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#ddd" />
          <XAxis dataKey="name" tick={{ fill: "#333", fontSize: 12 }} />
          <YAxis tick={{ fill: "#333", fontSize: 12 }} />
          <Tooltip cursor={{ fill: "rgba(0,0,0,0.05)" }} />
          <Bar dataKey="value" radius={[8, 8, 0, 0]}>
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default AboutChart;
