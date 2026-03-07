// Import helper functions from Sanity
// These are just helpers to define schemas cleanly
import { defineType, defineField } from 'sanity'

export default defineType({
  // Internal name Sanity uses
  // Think: database "type"
  name: 'page',

  // Human-readable name shown in the editor UI
  title: 'Page',

  // "document" means this is a top-level thing editors create
  // (as opposed to a nested object)
  type: 'document',

  fields: [
    // -----------------------
    // PAGE TITLE
    // -----------------------
    defineField({
      name: 'title',
      title: 'Page Title',
      type: 'string',

      // Validation: editor must fill this out
      validation: rule => rule.required()
    }),

    // -----------------------
    // SLUG (used by frontend)
    // -----------------------
    defineField({
      name: 'slug',
      title: 'URL Slug',
      type: 'slug',

      // Automatically generate slug from title
      // "About Page" → "about-page"
      options: {
        source: 'title'
      }
    }),

    // -----------------------
    // SECTIONS ON THE PAGE
    // -----------------------
    defineField({
      name: 'sections',
      title: 'Sections',
      type: 'array',

      // Each item in the array must be a "section"
      of: [{ type: 'section' }]
    })
  ]
})
