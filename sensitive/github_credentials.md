name = chikeraphaelnjokanma@gmail.com
password = ChilordCalculus7
site = github
sanity project Id = cals0fq
sanity project dataset = production
(I signed into sanity with my Github credentials)
Gemini API KEY = AIzaSyDce1_NgK4GA0YeT--tZ0QWCk2-AnKRRnM
orc_key = 'Xh84PtDmGYycPnlLCyPLBVYBzpUZbPJdA2t2zxJhZKQ='
App SECRET KEY = orc_key
JS files that don't use Base_URL(whose routes would have to be changed):
All raw .JS files
Docker commands:
cd orc-content
sanity dev
python -m backend.Router
cd frontend
npm run dev