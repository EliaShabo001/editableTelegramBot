# 🎓 Telegram Quiz Bot System

A comprehensive Telegram bot system for creating and taking quizzes with two separate bots:
- **Teacher Bot**: For creating and managing quizzes
- **Student Bot** (@TestStudentCollegeBot): For students to take quizzes

## 🚀 Features

### Teacher Bot Features:
- ✅ Password-protected admin access
- ✅ Create quiz batches with multiple questions
- ✅ Set quiz duration and subject
- ✅ Choose between 4 or 5 answer choices per question
- ✅ Generate unique one-time-use quiz links
- ✅ View all created quizzes
- ✅ Edit existing questions and answers
- ✅ Reactivate expired quiz links
- ✅ Automatic link expiration after use

### Deployment Features:
- ✅ Webhook-based architecture for cloud deployment 🆕
- ✅ Google Cloud Run ready with auto-scaling 🆕
- ✅ Local development mode with polling 🆕
- ✅ Containerized deployment with Docker 🆕

### Student Bot Features:
- ✅ Take quizzes via unique links
- ✅ 60-second timer per question
- ✅ Real-time scoring and feedback
- ✅ Detailed results with percentage
- ✅ Prevention of link reuse

## 📋 Database Schema

The system uses Supabase with three main tables:

### 1. `batch_links`
```sql
batch_links {
    batch_id TEXT PRIMARY KEY,
    link_token TEXT,
    telegram_link TEXT,
    used BOOLEAN
}
```

### 2. `batches_metadata`
```sql
batches_metadata {
    batch_id TEXT,
    subject TEXT,
    number_of_questions INT,
    duration_minutes INT
}
```

### 3. `questions`
```sql
questions {
    id INT PRIMARY KEY,
    question TEXT,
    options TEXT[],
    answer TEXT,
    batch_id TEXT,
    link_token TEXT,
    used BOOLEAN,
    subject TEXT
}
```

## 🛠️ Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Database
- Update `db.py` with your Supabase credentials
- Ensure all three tables are created in your Supabase database

### 3. Bot Tokens
- **Teacher Bot Token**: Already configured in `TelegramBot.py`
- **Student Bot Token**: `8042475385:AAGipEjvwZrxlibKGRtcoQFGYEYJWb9amBE`

### 4. Run the System

#### Option 1: Run Both Bots Together
```bash
python run_bots.py
```

#### Option 2: Run Bots Separately
```bash
# Terminal 1 - Teacher Bot
python TelegramBot.py

# Terminal 2 - Student Bot  
python StudentBot.py
```

## 📱 How to Use

### For Teachers:

1. **Authentication**: When you first start the bot, enter the admin password
2. **Create Questions**: Send `/insertQuestions` to the teacher bot
3. **Follow the wizard**:
   - Enter subject name
   - Set quiz duration (minutes)
   - Choose number of answer choices (4 or 5)
   - Specify number of questions
   - Add each question with your chosen number of options
   - Select correct answer (1-4 or 1-5)

3. **Get Quiz Link**: After completion, you'll receive a unique link like:
   ```
   https://t.me/TestStudentCollegeBot?start=quiz_TOKEN
   ```

4. **View All Quizzes**: Send `/Questions` to see all created quizzes

5. **Reactivate Expired Links**: Send `/ActiveQuestionLinkAgain` to:
   - View all quiz batches with their current status (Active/Used)
   - Reactivate expired quiz links for reuse
   - Get the reactivated link to send to new students

### For Students:

1. **Receive Link**: Get the quiz link from your teacher
2. **Start Quiz**: Click the link or send `/start` to @TestStudentCollegeBot
3. **Take Quiz**: 
   - Answer each question within 60 seconds
   - Get immediate feedback
   - See final results with percentage

## ⚠️ Important Notes

- **Security**: Teacher bot is password-protected - only authorized users can access admin features
- **Student Access**: Students can still access quizzes via links without authentication
- **One-Time Use**: Each quiz link can only be used once
- **Timer**: Each question has a 60-second time limit
- **Auto-Progress**: If time runs out, the quiz automatically moves to the next question
- **Results**: Students get detailed results including percentage and time taken

## 🔧 Bot Commands

### Teacher Bot Commands:
- `/start` - Welcome message with organized command menu
- `/insertQuestions` - Create a new quiz batch
- `/Questions` - View all created quizzes
- `/EditQuestion` - Edit existing quiz questions
- `/ActiveQuestionLinkAgain` - Reactivate expired quiz links 🆕
- `/test` - Test with existing questions (if any)

### Student Bot Commands:
- `/start` - Welcome message or start quiz with token
- `/startquiz quiz_TOKEN` - Alternative way to start quiz

## 🎯 Quiz Flow

1. **Teacher creates quiz** → Gets unique link
2. **Teacher shares link** with student
3. **Student clicks link** → Redirected to @TestStudentCollegeBot
4. **Student takes quiz** → Gets results
5. **Link expires** → Cannot be used again

## 🚀 Deployment Options

### Local Development
```bash
# Run locally with polling
python run_local.py
```

### Google Cloud Run - Option 1: Webhooks (Most Efficient)
```bash
# Deploy with webhooks (pay per request)
gcloud builds submit --config cloudbuild.yaml
```
- ✅ Most cost-effective for low/medium traffic
- ✅ Scales to zero when idle
- ❌ Requires webhook setup

### Google Cloud Run - Option 2: Polling + Keep-Alive (Simplest)
```bash
# Deploy with polling + keep-alive (always running)
gcloud builds submit --config cloudbuild-polling.yaml
```
- ✅ Simple setup, no webhook configuration
- ✅ Works exactly like local development
- ❌ Slightly higher cost (runs continuously)

### Deployment Guides
- **Webhooks**: See [DEPLOYMENT.md](DEPLOYMENT.md)
- **Polling + Keep-Alive**: See [POLLING-KEEPALIVE-DEPLOYMENT.md](POLLING-KEEPALIVE-DEPLOYMENT.md)

## 🔧 Architecture

- **Local Mode**: Uses polling (bot.polling()) for development
- **Production Mode**: Uses webhooks with Flask for cloud deployment
- **Database**: Supabase for persistent storage
- **Security**: Password-protected admin access

## 🔒 Security Features

- **Password Protection**: Admin commands require authentication
- **Link Expiration**: Each link works only once
- **Token Validation**: Invalid tokens are rejected
- **Database Integrity**: Prevents duplicate entries
- **User Session Management**: Proper cleanup after quiz completion

## 📊 Results Format

Students receive detailed results including:
- ✔️ Correct answers count
- ❌ Incorrect answers count  
- 📈 Percentage score
- ⏱️ Time taken
- 🎉 Performance feedback

## 🐛 Troubleshooting

### Common Issues:
1. **"Link already used"** - Each link works only once, get a new link
2. **"Invalid link"** - Check the token format and database connection
3. **Bot not responding** - Ensure both bots are running and tokens are correct

### Database Issues:
- Check Supabase connection in `db.py`
- Verify all tables exist with correct schema
- Ensure proper permissions are set

## 📝 File Structure

```
├── TelegramBot.py      # Teacher bot (create quizzes)
├── StudentBot.py       # Student bot (take quizzes)  
├── db.py              # Database operations
├── run_bots.py        # Run both bots together
├── requirements.txt   # Python dependencies
├── README.md          # This file
├── GUI.py            # (Optional GUI interface)
└── questions.json    # (Legacy question storage)
```

## 🤝 Support

For issues or questions:
1. Check the troubleshooting section
2. Verify database connection
3. Ensure bot tokens are correct
4. Check that all dependencies are installed
"# TelegramBotForCellege" 
"# editableTelegramBot" 
