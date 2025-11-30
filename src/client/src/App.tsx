import { useQuery } from "@tanstack/react-query";
import { IUser } from "./interfaces/IUser";
import request from "./utils/api";


const App = () => {
  const {data : user, isLoading} = useQuery({
    queryKey: ["user"],
    queryFn: async () => (await request("users/get")).data,
    select: (data) => data.user as IUser,
  });

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