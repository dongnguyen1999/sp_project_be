-- SQLite
INSERT INTO Question(QuestionID, Description, ActiveStatus, PartStatus, QuestionTotalMark, ArchivedBy, AddedBy, Question, UpdatedBy)
VALUES 
  (10, 'This questions about Activation Functions in Machine Learning Concepts', true, true, 3, null, null, 'Why is the ReLU function not differentiable at x=0?', null),
  (11, 'Machine Learning is one of the most sought after skills these days. If you are a data scientist, then you need to be good at Machine Learning – no two ways about it.', true, true, 2, null, null, '(a) What is Data Mining?', null),  
  (12, '', true, false, 2, null, null, 'What is the purpose of regression analysis?', null),
  (15, '', true, false, 2, null, null, 'What is deep learning?', null),
  (13, '', true, false, 3, null, null, 'What are machine learning and data science?', null),
  (14, '', true, false, 1, null, null, 'Why do you and other people sometimes implement machine learning algorithms from scratch?', null);