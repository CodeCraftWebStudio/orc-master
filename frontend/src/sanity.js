import { createClient } from '@sanity/client' 
import  { createImageUrlBuilder as imageUrlBuilder}  from '@sanity/image-url'
// Create a reusable Sanity client
export const sanity = createClient({
  // Your Sanity project ID
  projectId: 'cals0fq9',

  // Dataset name
  dataset: 'production',

  // API version (locks behavior)
  apiVersion: '2024-01-01',

  // Use Sanity CDN for faster + cached reads
  useCdn: true
})
const builder = imageUrlBuilder(sanity);
// GROQ query (Sanity's query language)
const real_query = `
*[
  _type == "page" &&
  slug.current == "about"
][0] {
  title,
  sections
}
`
const looser_query = `
*[
  _type in ["page", "pages"] &&
  slug.current == "about"
][0]{
  title,
  sections
}
 `

const loosest_query = `*[]`
export async function fetchAboutPage() {
  return sanity.fetch(loosest_query);
}

export const urlFor = (source) => builder.image(source);

// // Wrap fetch in an async function
// export async function fetchAboutPage() {
//   const page = await sanity.fetch(real_query)
//   return page
// }
