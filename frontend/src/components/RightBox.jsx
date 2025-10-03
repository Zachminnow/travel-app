
import { Button } from "./Button";
export const RightBox = () => {
  return (
    <div className="w-[100%] flex justify-center items-start flex-col gap-6">
      <h3 className="text-lg border-pink-600 font-semibold border-l-2 pl-2 text-[#2E2E2E]">About Us</h3>

      <h1 className="text-2xl font-bold text-pink-600 font-allan ">Discover Your Next Adventure</h1>

      <p className="text-[#2E2E2E]">
        Far far away, behind the word mountains, far from the countries Vokalia
        and Consonantia, there live the blind texts. Separated they live in
        Bookmarksgrove right at the coast of the Semantics, a large language
        ocean. A small river named Duden flows by their place and supplies it
        with the necessary regelialia. It is a paradisematic country, in which
        roasted parts of sentences fly into your mouth. Even the all-powerful
        Pointing has no control about the blind texts it is an almost
        unorthographic. Italic Mountains, she had a last view back on the
        skyline
      </p>
      <Button text="Read More" />
    </div>
  );
};
