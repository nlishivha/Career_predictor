-- Create a table to store user information
CREATE TABLE Users (
    UserID SERIAL PRIMARY KEY,
    Email VARCHAR(255) NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Username VARCHAR(255)
);

-- Create a table to store educational background
CREATE TABLE EducationalBackground (
    EduID SERIAL PRIMARY KEY,
    UserID INT REFERENCES Users(UserID),
    Level VARCHAR(255),
    QualificationName VARCHAR(255)
);

-- Create a table to store user skills
CREATE TABLE UserSkills (
    SkillID SERIAL PRIMARY KEY,
    UserID INT REFERENCES Users(UserID),
    SkillName VARCHAR(255)
);

-- Create a table to store user job preferences
CREATE TABLE UserJobPreferences (
    JobPrefID SERIAL PRIMARY KEY,
    UserID INT REFERENCES Users(UserID),
    JobPreferenceName VARCHAR(255)
);

-- Create a table to store user work experience
CREATE TABLE UserExperience (
    ExpID SERIAL PRIMARY KEY,
    UserID INT REFERENCES Users(UserID),
    FieldName VARCHAR(255),
    Experience VARCHAR(255)
);

-- Create a table to store user feedback
CREATE TABLE UserFeedback (
    FeedbackID SERIAL PRIMARY KEY,
    UserID INT REFERENCES Users(UserID),
    FeedbackText TEXT
);


-- Define foreign key constraints to link the tables
ALTER TABLE EducationalBackground
ADD FOREIGN KEY (UserID) REFERENCES Users (UserID);

ALTER TABLE UserSkills
ADD FOREIGN KEY (UserID) REFERENCES Users (UserID);

ALTER TABLE UserJobPreferences
ADD FOREIGN KEY (UserID) REFERENCES Users (UserID);

ALTER TABLE UserExperience
ADD FOREIGN KEY (UserID) REFERENCES Users (UserID);

ALTER TABLE UserFeedback
ADD FOREIGN KEY (UserID) REFERENCES Users (UserID);
