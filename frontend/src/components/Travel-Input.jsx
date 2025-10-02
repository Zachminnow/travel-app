

export const TravelInput = () => {
  const months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
  ];
  return (
    <div className="bg-slate-900 p-4 rounded-lg shadow-lg w-[1180px] flex content-evenly gap-5">
      <input
        type="text"
        placeholder="Search for destinations..."
        className="p-2 border border-gray-300 rounded-md"
      />
      <div className="flex bg-slate-50 rounded-lg border-[2px] border-pink-400 justify-center items-center">
        <i className="fa-solid fa-location-dot text-pink-400 mx-2"></i>
        <p className="p-3">When</p>
        <select className="p-2 border border-gray-300 rounded-md mx-2 ">
          {months.map((month, index) => (
            <option key={index} value={month}>
              {month}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
};
