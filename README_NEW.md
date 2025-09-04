# py-aishell-engine

An intelligent shell interface that understands natural language commands and translates them to system operations with built-in safety mechanisms.

## 🎯 Vision

Create a terminal that users can interact with using natural language while maintaining the power and flexibility of traditional command-line interfaces.

## 📋 Current Status

### ✅ Completed Features
- **Basic GUI Interface** (PyQt5-based terminal)
- **Command Engine Architecture** (4-stage pipeline)
- **Natural Language Processing** (Pattern-based, limited)
- **Safety System** (Risk assessment and confirmations)
- **Cross-platform Support** (Windows/Unix commands)

### ⚠️ Current Limitations
- **Hardcoded pattern matching** - Cannot scale to handle all natural language variations
- **Limited context understanding** - No conversation memory or clarification system
- **Basic safety confirmations** - Generic messages without detailed operation info

## 🚀 Next Phase: NLP Integration

The current regex-based approach is being replaced with a proper NLP-driven system. See [`NLP_COMMAND_ENGINE_ROADMAP.md`](NLP_COMMAND_ENGINE_ROADMAP.md) for detailed plans.

### Planned Improvements
1. **True NLP Understanding** using spaCy/Transformers
2. **Intelligent Clarification** when commands are ambiguous  
3. **Enhanced Safety System** with detailed operation previews
4. **Context Awareness** and conversation memory
5. **Learning System** that adapts to user preferences

## 🏗️ Architecture

```
User Input (Natural Language)
          ↓
    [NLP Processor] ← Will replace regex patterns
          ↓
    [Intent Mapper] 
          ↓
    [Safety Validator] ← Enhanced with detailed confirmations
          ↓
    [Command Executor]
          ↓
    System Operations
```

## 📁 Project Structure

```
py-aishell-engine/
├── engine/          # Core command processing logic
│   ├── executor.py  # Main command engine orchestration
│   ├── preprocessor.py # Input processing (to be replaced with NLP)
│   ├── mapper.py    # Command mapping (to be redesigned)
│   └── safety.py    # Safety validation system
├── gui/             # PyQt5 user interface
├── system/          # System interaction utilities  
├── tests/           # Test suites
└── docs/            # Documentation and roadmaps
```

## 🔧 Installation

```bash
# Clone the repository
git clone https://github.com/Merril1704/py-aishell-engine.git
cd py-aishell-engine

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## 💡 Example Usage (Current)

```
> list files in folder games on drive d
> create folder called "My Project" 
> go to directory Documents
> show me all files here
> copy report.pdf to backup folder
```

## 🔮 Future Usage (After NLP Integration)

```
> Can you show me what's in my games folder on the D drive?
> I need to backup all my documents from last week
> Find any files that might be taking up too much space
> Create a new project folder and copy my template files there
```

## 🛡️ Safety Features

- **Risk Assessment**: Operations are categorized by risk level
- **Confirmation System**: Dangerous operations require explicit confirmation
- **Protected Paths**: Critical system directories are protected
- **Detailed Previews**: Shows exactly what will be affected before execution

## 🤝 Contributing

This project is in active development. The current focus is on implementing the NLP-based command understanding system outlined in the roadmap.

## 📄 License

MIT License - Feel free to use and modify as needed.

---

**Note**: This is a development version. The command engine is being redesigned for better natural language understanding. See the roadmap for upcoming improvements.
