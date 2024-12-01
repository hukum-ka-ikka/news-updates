import { useEffect } from "react";
import { useState } from "react";
import NewsCard from "./NewsCard";
import toast from "react-hot-toast";

const NewsFeed = () => {
  const [newsFeed, setNewsFeed] = useState([]);

  const backend_url = import.meta.env.VITE_BACKEND_URL

  useEffect(() => {
    const eventSource = new EventSource(backend_url);

    eventSource.onmessage = function (event) {
      try {
        const data = JSON.parse(event.data); // Parse the incoming JSON data
        console.log("Updating news feed");
        setNewsFeed(data); // Update the state with the new data
        toast.success("Feed Updated")
      } catch (error) {
        toast.success("Feed Update Failed")
        console.error("Error parsing the event data:", error);
      }
    };

    eventSource.onerror = function (event) {
      console.error("Error receiving SSE:", event);
    };

    return () => {
      eventSource.close(); // Close the connection when the component unmounts
    };
  }, []);
  
  return (
    <div className="flex gap-5 flex-wrap justify-center max-w-[1250px]">
      {newsFeed &&
        newsFeed.map((article, index) => (
          <NewsCard key={index} article={article} />
        ))}
    </div>
  );
};

export default NewsFeed;
