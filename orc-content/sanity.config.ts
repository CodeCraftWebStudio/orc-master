import {defineConfig} from 'sanity'
import {structureTool} from 'sanity/structure'
import {visionTool} from '@sanity/vision'
import {schemaTypes} from './schemas' 
import { muxInput } from 'sanity-plugin-mux-input';
export default defineConfig({
  name: 'default',
  title: 'orc-content',

  projectId: 'cals0fq9',
  dataset: 'production',

  plugins: [structureTool(), visionTool(), muxInput()],

  schema: {
    types: schemaTypes,
  },
})
export const MUX_API_KEY = "forssn1f5s2oiqa6ioa7dk8l1";