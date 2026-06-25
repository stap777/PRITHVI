"""
System File Utilities.

This module provides utility helpers for filesystem interactions, safe binary writes,
and directory compression routines.

Functions:
    ensure_dir: Verifies and builds path folder structure.
    save_uploaded_file: Safely streams incoming bytes from HTTP file uploads to disk.
    zip_directory: Packs folder contents into a single ZIP archive.

TODO:
    * Implement MD5 checksum checks on written files.
"""

import shutil
import zipfile
from pathlib import Path
from loguru import logger


def ensure_dir(path: Path) -> Path:
    """
    Creates target directory if it does not already exist.
    """
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created directory: {path}")
    return path


def save_uploaded_file(file_bytes: bytes, destination_path: Path) -> int:
    """
    Safely writes raw input data bytes to a specific filesystem path.
    
    Args:
        file_bytes: Streamed file bytes.
        destination_path: Local write path on disk.
        
    Returns:
        Written file size in bytes.
    """
    logger.info(f"Writing file data to local path: {destination_path}")
    
    # Ensure parent folder structure exists
    ensure_dir(destination_path.parent)
    
    with open(destination_path, "wb") as buffer:
        bytes_written = buffer.write(file_bytes)
        
    logger.info(f"Successfully wrote {bytes_written} bytes to {destination_path.name}")
    return bytes_written


def zip_directory(source_dir: Path, output_zip_path: Path) -> Path:
    """
    Compresses target directory contents into a ZIP archive.
    
    Args:
        source_dir: Directory containing target files to package.
        output_zip_path: Destination path for target ZIP file.
    """
    logger.info(f"Compiling ZIP archive for directory: {source_dir} -> {output_zip_path}")
    
    if not source_dir.exists():
        raise FileNotFoundError(f"Source folder does not exist: {source_dir}")
        
    ensure_dir(output_zip_path.parent)
    
    with zipfile.ZipFile(output_zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file_path in source_dir.rglob("*"):
            # Avoid packing the output archive itself if created inside the same folder
            if file_path == output_zip_path:
                continue
            zipf.write(file_path, file_path.relative_to(source_dir))
            
    logger.info(f"ZIP package successfully created at: {output_zip_path}")
    return output_zip_path
