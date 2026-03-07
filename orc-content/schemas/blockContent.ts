import { defineType } from 'sanity'

export default defineType({
  // Internal name
  name: 'blockContent',

  // This is an array of blocks
  type: 'array',

  // Allowed block types
  of: [
    {
      // Normal rich text
      // headings, paragraphs, lists, links, etc.
      type: 'block'
    },
    {
      // Images
      type: 'image',

      // Lets editors crop images nicely
      options: { hotspot: true }
    }
  ]
})
