// server/factcheck.js
import axios from "axios"
import dotenv from "dotenv"
dotenv.config()

export const checkFact = async (query) => {
  const apiKey = process.env.GOOGLE_FACTCHECK_API_KEY

  try {
    const url = `https://factchecktools.googleapis.com/v1alpha1/claims:search?query=${encodeURIComponent(query)}&key=${apiKey}`
    const response = await axios.get(url)
    const claims = response.data.claims || []

    if (claims.length === 0) {
      return { status: "UNVERIFIED", source: null, rating: null, url: null }
    }

    // Loop through claim reviews and choose the most relevant one
    let bestClaim = null
    let bestReview = null

    for (const claim of claims) {
      if (claim.claimReview && claim.claimReview.length > 0) {
        for (const review of claim.claimReview) {
          // Prioritize definitive ratings (true/false) over mixed ratings
          const textualRating = review.textualRating.toLowerCase()
          if (!bestReview || textualRating.includes("true") || textualRating.includes("false")) {
            bestClaim = claim
            bestReview = review
          }
        }
      }
    }

    if (!bestReview) {
      return { status: "UNVERIFIED", source: null, rating: null, url: null }
    }

    const textualRating = bestReview.textualRating.toLowerCase()
    let status = "UNVERIFIED" // default

    if (textualRating.includes("true") && !textualRating.includes("mostly") && !textualRating.includes("half")) {
      status = "TRUE"
    } else if (textualRating.includes("false") || textualRating.includes("pants on fire")) {
      status = "FALSE"
    } else if (textualRating.includes("mostly true") || textualRating.includes("mostly correct")) {
      status = "MOSTLY_TRUE"
    } else if (textualRating.includes("mostly false") || textualRating.includes("mostly incorrect")) {
      status = "MOSTLY_FALSE"
    } else if (textualRating.includes("half")) {
      status = "MIXED"
    } else {
      status = "UNVERIFIED"
    }

    return {
      status,
      source: bestReview.publisher.name,
      rating: bestReview.textualRating,
      url: bestReview.url,
      claimDate: bestClaim.claimDate || null,
      claimant: bestClaim.claimant || null,
    }
  } catch (err) {
    console.error("Fact Check API error:", err.message)
    return { status: "UNVERIFIED", source: null, rating: null, url: null }
  }
}
