import NavBar from "./components/NavBar"
import NewsFeed from "./components/NewsFeed"

function App() {
  return (
    <div className="flex flex-col gap-4 items-center justify-center w-full pb-10">
        <NavBar />
        <NewsFeed />
    </div>
  )
}

export default App
