CREATE TABLE FastaFileDb (
  fid INTEGER PRIMARY KEY,
  fastaFile VARCHAR(100) NOT NULL,
  species VARCHAR(100),
  country VARCHAR(100)
);

CREATE TABLE fidBodyPartMap (
  fid INTEGER NOT NULL,
  bodyPart VARCHAR(100) NOT NULL,
  PRIMARY KEY (fid, bodyPart)
);

CREATE TABLE fidKeywordMap (
  fid INTEGER NOT NULL,
  keyword VARCHAR(100) NOT NULL,
  PRIMARY KEY (fid, keyword)
);


CREATE TABLE humanReferenceGenome (
  chromosomeNo INTEGER PRIMARY KEY,
  file VARCHAR(100) NOT NULL
);

-- insert
INSERT INTO FastaFileDb VALUES (0001, 'hemoglobin subunit beta [ Homo sapiens (human) ]', 'Homo sapiens', "India");
INSERT INTO FastaFileDb VALUES (0002, 'hemoglobin subunit beta [ Gorilla gorilla gorilla (western lowland gorilla) ]', 'Gorilla gorilla gorilla', "Uganda");
INSERT INTO FastaFileDb VALUES (0003, 'hemoglobin subunit beta [ Gadus morhua (Atlantic cod) ]', 'Gadus morhua', "USA");
INSERT INTO FastaFileDb VALUES (0004, 'hemoglobin beta, subunit rho [ Gallus gallus (chicken) ]', 'Gallus gallus', "spain");
INSERT INTO FastaFileDb VALUES (0005, 'Homo sapiens G protein-coupled receptor kinase 1 (GRK1), mRNA', 'Homo sapiens', "India");

INSERT INTO fidBodyPartMap VALUES (0001, 'Blood');
INSERT INTO fidBodyPartMap VALUES (0002, 'Blood');
INSERT INTO fidBodyPartMap VALUES (0003, 'Blood');
INSERT INTO fidBodyPartMap VALUES (0004, 'Blood');
INSERT INTO fidBodyPartMap VALUES (0005, 'Eye');

INSERT INTO fidKeywordMap VALUES (0001, 'Blood');
INSERT INTO fidKeywordMap VALUES (0001, 'hemoglobin');
INSERT INTO fidKeywordMap VALUES (0005, 'Eye');
INSERT INTO fidKeywordMap VALUES (0005, 'light receptor');
