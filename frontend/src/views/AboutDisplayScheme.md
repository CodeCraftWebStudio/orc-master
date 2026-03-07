When we load the about page from Sanity(it's unfortunate this thing is driving me rather crazy), we get something like this:
```json
{
  "_createdAt": "2025-12-23T12:58:27Z",
  "_id": "8610a0e5-b5de-44d9-814f-c34b82d4edd1",
  "_rev": "bmeyIsrHFvhmvMeI2BAYWr",
  "_type": "page",
  "_updatedAt": "2025-12-27T17:20:52Z",
  "_system": {
    "publishedAt": "2025-12-27T17:00:00Z",
    "version": 1
  },
  "title": "About Us",
  "sections": [
    {
      "_key": "xyz1",
      "title": "Our History",
      "body": [
        {
          "_type": "block",
          "children": [
            { "_key": "c1", "text": "Founded in 1999, we started as a small startup...", "_type": "span" }
          ],
          "markDefs": [],
          "style": "normal"
        },
        {
          "_type": "block",
          "children": [
            { "_key": "c2", "text": "Over the years, we expanded globally.", "_type": "span" }
          ],
          "markDefs": [],
          "style": "normal"
        }
      ]
    },
    {
      "_key": "xyz2",
      "title": "Our Mission",
      "body": [
        {
          "_type": "block",
          "children": [
            { "_key": "c3", "text": "Our mission is to deliver sustainable products.", "_type": "span" }
          ],
          "markDefs": [],
          "style": "normal"
        },
        {
          "_type": "block",
          "children": [
            { "_key": "c4", "text": "We aim to innovate while keeping the environment in mind.", "_type": "span" }
          ],
          "markDefs": [],
          "style": "normal"
        }
      ]
    }
  ]
}
```
And we want to achieve 2 main stylistic goals:
1. An interactive, clean sidebar
2. A page that is clean and can easily display rich text, images, (maybe even videos) and more

From the json above, we can get that:
page[x]_title = result[x].title
page[x]_section[y]_title = result[x].sections[y].title
page[x]_section[y]_content(all children) = result[x].sections[y].body.children <- This is going to return an array per style(stoppinig at .body is per paragraph). To render text correctly, therefore, we could say:
```python
page = result[x]
for section in page.sections:
    print(section.title)

    for block in section.body:
        paragraphText = ""

        for span in block.children:
            paragraphText += span.text

        renderParagraph(
            block
        )

```
Part 2: Scroll Spy and sidebar
```console
sections = all <section> elements

observe sections

when section crosses activation line:
    activeSectionKey = section.dataset.key

Sidebar highlights the button where :
    button.key == activeSectionKey


```

Part 3: Rendering
