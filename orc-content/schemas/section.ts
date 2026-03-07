import { defineType, defineField } from 'sanity'

export default defineType({
  // Internal name
  name: 'section',

  // What editors see
  title: 'Section',

  // "object" means:
  // ❗ this cannot exist on its own
  // ❗ it only lives inside another document (like Page)
  type: 'object',

  fields: [
    // -----------------------
    // SECTION TITLE
    // -----------------------
    defineField({
      name: 'title',
      title: 'Section Title',
      type: 'string'
    }),

    // -----------------------
    // MAIN CONTENT
    // -----------------------
    defineField({
      name: 'blocks',
      title: 'Content',
      type: 'blockContent'
    }),

    // -----------------------
    // SUBSECTIONS
    // -----------------------
    defineField({
      name: 'children',
      title: 'Subsections',

      // Array of MORE sections
      // 🔁 This is recursion
      type: 'array',
      of: [{ type: 'section' }]
    })
  ]
})
