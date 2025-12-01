import {useQuery} from "@tanstack/react-query";
import request from "./utils/api";
import type { IUser } from "./interfaces/IUser";
import  {init, initData, viewport} from "@tma.js/sdk";

init();
viewport.mount();

initData.restore();
viewport.expand();

const App=() => {
  const {data:user, isLoading} = useQuery({
    queryKey: ["user"],
    queryFn:async () => {
      return (await request("users/get")).data;
    },
    select: (data) => data.user as IUser
  })

return (
    <div className="h-screen flex justify-center items-center text-white text-3xl">
      {isLoading ? (
        <div className="animate-pulse">Loading...</div>
      ) : (
        <div>{user?.name}</div>
      )}
    </div>
  );
};


export default App;