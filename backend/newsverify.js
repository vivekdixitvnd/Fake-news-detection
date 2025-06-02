// ✅ Fully Fixed newsverify.js
import axios from "axios"
import dotenv from "dotenv"
dotenv.config()

export const verifyWithNewsSources = async (query) => {
  const apiKey = process.env.NEWS_API_KEY

  try {
    const response = await axios.get("https://newsapi.org/v2/everything", {
      params: {
        q: query,
        language: "en",
        sortBy: "relevancy",
        pageSize: 5,
        apiKey: apiKey,
      },
    })

    const articles = response.data.articles || []

    if (articles.length === 0) {
      return {
        status: "UNVERIFIED",
        source: null,
        link: null,
        title: null,
        publishedAt: null,
        allSources: [],
      }
    }

    const topArticle = articles[0]
    const allSources = articles.map((article) => ({
      source: article.source.name,
      title: article.title,
      url: article.url,
      publishedAt: article.publishedAt,
    }))

    return {
      status: "REAL",
      source: topArticle.source.name,
      link: topArticle.url,
      title: topArticle.title,
      publishedAt: topArticle.publishedAt,
      allSources: allSources,
    }
  } catch (err) {
    console.error("News API error:", err.message)
    return {
      status: "UNVERIFIED",
      source: null,
      link: null,
      title: null,
      publishedAt: null,
      allSources: [],
    }
  }
}
