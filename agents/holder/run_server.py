import os
import sys

# Set working directory
os.chdir(r"F:\Projects\MVJ\studio-main\CryptLocker_Jovian786\agents\holder")
sys.path.insert(0, r"F:\Projects\MVJ\studio-main\CryptLocker_Jovian786\agents\holder")

# Start uvicorn
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8031,
        reload=True,
        log_level="info"
    )
