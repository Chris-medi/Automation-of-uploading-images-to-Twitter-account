```markdown:
# Twitter Image Upload Automation

An automated system for generating and uploading AI-generated images to Twitter using local LLM models.

## Features

- 🤖 Local LLM processing with Ollama
- 🖼️ Automated image generation
- 🐦 Twitter integration for automatic posting
- 📝 Smart prompt generation and refinement
- 🔄 Efficient package management with uv

## Models Used

- **phi4**: Status generation and initial prompts
- **llama3.2:3b**: Prompt refinement and structured output


## Stable Diffusion WebUI Setup

1. Install Stable Diffusion WebUI from [AUTOMATIC1111/stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui)

2. Start WebUI with API access:
```bash
python launch.py --api --nowebui --xformers
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Chris-medi/Automation-of-uploading-images-to-Twitter-account.git
cd Automation-of-uploading-images-to-Twitter-account
```

2. Install uv:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

3. Create and activate virtual environment:
```bash
uv venv
.venv/Scripts/activate
```

4. Install dependencies:
```bash
uv sync
```

## Ollama Setup

1. Install Ollama from [ollama.ai](https://ollama.ai)

2. Download required models:
```bash
ollama pull phi4
ollama pull llama3.2:3b
```

## Configuration

Create a `.env` file:
```plaintext
BASE_URL_OLLAMA=base_url_ollama
BASE_URL=base_url # url api stable-diffusion-webui
API_KEY=your_api_key
API_SECRET_KEY=your_api_secret
BEARER_TOKEN=bearer_token
ACCESS_TOKEN=your_access_token
ACCESS_TOKEN_SECRET=your_access_token_secret
```

## Project Structure

```plaintext
.
├── output_images/
├── src/
│   ├── LLM/
│   │   ├── __init__.py
│   │   ├── ollama.py        # Ollama LLM implementations
│   │   ├── schemas.py       # Response schemas
│   │   └── templates.py     # Prompt templates
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── twitter.py
│   │   └── image.py        # Image processing utilities
│   └── __init__.py
├── settings/
│   ├── __init__.py
│   ├── LLM/
│   │   ├── __init__.py      # LLM configuration
│   └── config.py           # Configuration settings
├── .env                    # Environment variables
├── .gitignore
├── .python-version
├── main.py                # Main application entry
├── pyproject.toml
├── README.md
└── LICENSE                # GPL-2.0 License
└── uv.lock
```

## Usage

1. Start Ollama:
```bash
ollama serve
```

2. Run the application:
```bash
uv run main.py
```

## Scheduling Tasks

You can automate the image generation and posting process using cron jobs:

1. Open your crontab:
```bash
crontab -e
```

2. Add a schedule (example for running every 6 hours):
```bash
0 */6 * * * cd /path/to/project && /path/to/venv/bin/python main.py
```

Common scheduling patterns:
- Every hour: `0 * * * *`
- Daily at midnight: `0 0 * * *`
- Every Sunday: `0 0 * * 0`
- Every month: `0 0 1 * *`


## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add YourFeature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

## License

This project is licensed under the GNU General Public License v2.0 - see the [LICENSE](LICENSE) file for details.

For more information about GPL-2.0, visit: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
```

And here's the GPLv2 license file:

```plaintext:\\wsl.localhost\Ubuntu\home\chriss\project\automation-account-x\LICENSE
                    GNU GENERAL PUBLIC LICENSE
                       Version 2, June 1991

 Copyright (C) 2024 Chris-medi

 This program is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 2 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License along
 with this program; if not, write to the Free Software Foundation, Inc.,
 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
```


I'll add information about scheduling tasks with cron jobs to your README.
