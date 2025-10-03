export const InputBox = ({placeholder,type}) => {
  return (
    <div className="flex bg-slate-50 rounded-lg border-[1px] border-pink-600 justify-evenly items-center w-[300px]">
      <FaMapMarkerAlt className="text-pink-600 mx-2" size={24} />
      <input
        type={type}
        placeholder={placeholder}
        className="p-2 focus:outline-none border-[0] rounded-md"
      />
    </div>
  );
};


