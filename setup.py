import platform
import subprocess
import sys


def install_tesseract():
    """Install Tesseract OCR based on the user's operating system."""
    system = platform.system()

    try:
        if system == "Darwin":  # macOS
            print("Installing Tesseract OCR for macOS...")
            subprocess.run(["brew", "install", "tesseract"], check=True)

        elif system == "Linux":
            print("Installing Tesseract OCR for Linux...")
            subprocess.run(
                ["sudo", "apt-get", "install", "-y", "tesseract-ocr"], check=True
            )

        elif system == "Windows":
            print("Tesseract installation is required for Windows.")
            print(
                "Please download and install Tesseract manually from: https://github.com/UB-Mannheim/tesseract/wiki"
            )
        else:
            print("Unsupported OS. Please install Tesseract manually.")

    except subprocess.CalledProcessError as e:
        print(f"Error installing Tesseract: {e}")
        sys.exit(1)


def install_requirements():
    """Install Python dependencies from requirements.txt."""
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True
        )
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        sys.exit(1)


def verify_installation():
    """Verify that all dependencies are installed correctly."""
    try:
        import pytesseract  # noqa: F401
        import numpy  # noqa: F401

        print("\n✅ All dependencies installed successfully!")
    except ImportError as e:
        print(f"\n❌ Missing dependency: {e}. Please check your installation.")
        sys.exit(1)


if __name__ == "__main__":
    print("\n🔧 Setting up the project...\n")

    install_tesseract()
    install_requirements()
    verify_installation()

    print("\n🚀 Setup complete! You can now run the application.")
