--==============================================================
-- DBMS name:      ANSI Level 2
-- Created on:     5/11/2021 1:52:07 PM
--==============================================================


-- drop index CLASS_PK;

-- drop table Class cascade;

-- drop index QUESTION_PK;

-- drop table Question cascade;

-- drop index CONSIST_OF_FK;

-- drop index QUESTIONPART_PK;

-- drop table QuestionPart cascade;

-- drop index COMPRISES_FK;

-- drop index STUDENT_PK;

-- drop table Student cascade;

-- drop index ANSWER_BY_1_FK;

-- drop index ANSWER_FK;

-- drop index TRNQUEST_PK;

-- drop table TrnQuest cascade;

-- drop index ANSWER_BY_FK;

-- drop index ANSWER_1_FK;

-- drop index TRNQUESTPART_PK;

-- drop table TrnQuestPart cascade;

--==============================================================
-- Table: Class
--==============================================================
create table Class (
ClassID              INTEGER              not null,
Name                 VARCHAR(255),
NoOfStudent          INTEGER,
primary key (ClassID)
);

--==============================================================
-- Index: CLASS_PK
--==============================================================
create unique index CLASS_PK on Class (
ClassID ASC
);

--==============================================================
-- Table: Question
--==============================================================
create table Question (
QuestionID           INTEGER              not null,
Description          VARCHAR(500),
ModelAns             VARCHAR(255),
Question             VARCHAR(255),
ActiveStatus         smallint,
PartStatus           smallint,
QuestTotalMark    FLOAT(255),
ArchivedBy           VARCHAR(255),
UpdatedBy            VARCHAR(255),
AddedBy              VARCHAR(255),
primary key (QuestionID)
);

--==============================================================
-- Index: QUESTION_PK
--==============================================================
create unique index QUESTION_PK on Question (
QuestionID ASC
);

--==============================================================
-- Table: QuestionPart
--==============================================================
create table QuestionPart (
QuestionID           INTEGER              not null,
PartID               VARCHAR(255)         not null,
PartQuestion         VARCHAR(255),
PartModelAns         VARCHAR(255),
PartTotalMark        FLOAT(255),
primary key (QuestionID, PartID),
foreign key (QuestionID)
      references Question (QuestionID)
);

--==============================================================
-- Index: QUESTIONPART_PK
--==============================================================
create unique index QUESTIONPART_PK on QuestionPart (
QuestionID ASC,
PartID ASC
);

--==============================================================
-- Index: CONSIST_OF_FK
--==============================================================
create  index CONSIST_OF_FK on QuestionPart (
QuestionID ASC
);

--==============================================================
-- Table: Student
--==============================================================
create table Student (
StudID               INTEGER              not null,
ClassID              INTEGER              not null,
Name                 VARCHAR(255),
NRIC                 NUMERIC(50),
primary key (StudID),
foreign key (ClassID)
      references Class (ClassID)
);

--==============================================================
-- Index: STUDENT_PK
--==============================================================
create unique index STUDENT_PK on Student (
StudID ASC
);

--==============================================================
-- Index: COMPRISES_FK
--==============================================================
create  index COMPRISES_FK on Student (
ClassID ASC
);

--==============================================================
-- Table: TrnQuest
--==============================================================
create table TrnQuest (
StudID               INTEGER              not null,
QuestionID           INTEGER              not null,
Response             VARCHAR(255),
TrnMark              VARCHAR(255),
Reason               VARCHAR(255),
Other                VARCHAR(255),
ModeratedBy          DATE,
DateModerated        DATE,
DateMarked           DATE,
primary key (StudID, QuestionID),
foreign key (StudID)
      references Student (StudID),
foreign key (QuestionID)
      references Question (QuestionID)
);

--==============================================================
-- Index: TRNQUEST_PK
--==============================================================
create unique index TRNQUEST_PK on TrnQuest (
StudID ASC,
QuestionID ASC
);

--==============================================================
-- Index: ANSWER_FK
--==============================================================
create  index ANSWER_FK on TrnQuest (
StudID ASC
);

--==============================================================
-- Index: ANSWER_BY_1_FK
--==============================================================
create  index ANSWER_BY_1_FK on TrnQuest (
QuestionID ASC
);

--==============================================================
-- Table: TrnQuestPart
--==============================================================
create table TrnQuestPart (
StudID               INTEGER              not null,
QuestionID           INTEGER              not null,
PartID               VARCHAR(255)         not null,
PARTRESPONSE         VARCHAR(255),
Other                VARCHAR(255),
ModeratedBy          DATE,
DateModerated        DATE,
DateMarked           DATE,
Reason               VARCHAR(255),
primary key (StudID, QuestionID, PartID),
foreign key (StudID)
      references Student (StudID),
foreign key (QuestionID, PartID)
      references QuestionPart (QuestionID, PartID)
);

--==============================================================
-- Index: TRNQUESTPART_PK
--==============================================================
create unique index TRNQUESTPART_PK on TrnQuestPart (
StudID ASC,
QuestionID ASC,
PartID ASC
);

--==============================================================
-- Index: ANSWER_1_FK
--==============================================================
create  index ANSWER_1_FK on TrnQuestPart (
StudID ASC
);

--==============================================================
-- Index: ANSWER_BY_FK
--==============================================================
create  index ANSWER_BY_FK on TrnQuestPart (
QuestionID ASC,
PartID ASC
);

