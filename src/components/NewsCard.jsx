
/* eslint-disable react/prop-types */
const NewsCard = ({ article }) => {

    const handleCardClick = (url) => {
        window.open(url, '_blank'); // To open the Original news link in a different tab
      };

  return (
    <div onClick={() => handleCardClick(article.link)}
      className="flex flex-col gap-3 p-2 w-72 border rounded-xl transition-all duration-200 hover:cursor-pointer hover:scale-105"
      style={{ boxShadow: "1px 1px 10px #808080" }}
    >
      <img src={article.image} className="w-full rounded-lg" />
      <div className="flex flex-col gap-3 h-full justify-between">
        <div className="flex flex-col gap-1">
          <p className="leading-tight font-semibold">
            {article.title.slice(0, 30)}...
          </p>
          <p className="leading-tight ">{article.summary}</p>
        </div>

        <p className="text-sm">
          <span className="font-semibold">Published on:</span>{" "}
          {article.published}
        </p>
      </div>
    </div>
  );
};

export default NewsCard;
