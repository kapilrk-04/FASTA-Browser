import express from 'express';
import cors from 'cors';

import seqAlignRouter from './routes/seq_align.js';

const app = express();
const port = process.env.PORT || 3000;

app.use(cors());

app.use(express.json());

//uniqueness: method and URL

app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept');
  next();
});

app.use('/api/seq_align', seqAlignRouter);

// Start server
app.listen(port, () => {
    console.log(`Server listening at http://localhost:${port}`);
});
