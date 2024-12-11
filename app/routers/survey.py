from fastapi import APIRouter, HTTPException
from app.database.excel_db import SurveyDatabase
from app.schemas.models import Question, SurveyResponse
import logging
from fastapi.responses import FileResponse
import os
from pathlib import Path
import shutil

router = APIRouter()
db = SurveyDatabase("app/database/Database.xlsx")

# Initialize icon directories
def init_icon_directories():
    # Updated paths without double 'app'
    static_dir = Path("static")
    icon_dir = static_dir / "icon"
    school_icon_dir = static_dir / "school_icon"

    # Create directories if they don't exist
    static_dir.mkdir(parents=True, exist_ok=True)
    icon_dir.mkdir(parents=True, exist_ok=True)
    school_icon_dir.mkdir(parents=True, exist_ok=True)

    # Copy default icons if they don't exist
    default_icon_path = icon_dir / "default.png"
    default_school_icon_path = school_icon_dir / "default.png"

    # Updated backup path
    backup_icon_dir = Path("backup/icons")
    if backup_icon_dir.exists():
        for icon_file in backup_icon_dir.glob("*.png"):
            target_path = icon_dir / icon_file.name
            if not target_path.exists():
                shutil.copy2(icon_file, target_path)

# Initialize directories when the module loads
init_icon_directories()

@router.get("/questions")
async def get_questions():
    try:
        questions = db.get_all_questions()
        return questions
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching questions: {str(e)}"
        )

@router.post("/submit")
async def submit_survey(response: SurveyResponse):
    try:
        # Get the basic results from your database
        basic_result = db.process_basic_results(response.answers)
        
        # Get personality type data
        personality_data = basic_result.get("personality_type", {})
        
        # Calculate RIASEC scores (normalized between 0 and 1)
        category_counts = basic_result.get("category_counts", {})
        max_score = max(category_counts.values()) if category_counts.values() else 1
        riasec_scores = {
            category: count / max_score
            for category, count in category_counts.items()
        }

        # Get unique industries based on industry name
        seen_industries = set()
        unique_industries = []
        for industry in basic_result.get("recommended_industries", []):
            industry_name = industry.get("industry")
            if industry_name and industry_name not in seen_industries:
                seen_industries.add(industry_name)
                unique_industries.append(industry)

        def parse_jupas_info(jupas_str):
            try:
                if not jupas_str:
                    return None
                    
                # Remove extra whitespace and split by '//'
                parts = [part.strip() for part in jupas_str.split('//') if part.strip()]
                
                if len(parts) >= 4:  # We expect 4 parts: subject, code, school, score
                    jupas_info = {
                        "subject": parts[0],
                        "jupasCode": parts[1],
                        "school": parts[2],
                        "averageScore": f"{parts[3]}/7.0"
                    }
                    return jupas_info
                else:
                    return None
                    
            except Exception as e:
                return None

        def parse_career_paths(career_paths):
            if not career_paths:
                return []
            
            # If it's already a list, return it directly
            if isinstance(career_paths, list):
                return [path.strip() for path in career_paths if path.strip()]
            
            # If it's a string, split it by '//'
            if isinstance(career_paths, str):
                return [path.strip() for path in career_paths.split('//') if path.strip()]
            
            return []

        # Format the analysis result
        analysis_result = {
            "personality": {
                "type": personality_data.get("role", "Default Type"),
                "description": personality_data.get("who_you_are", "Default description"),
                "interpretation": personality_data.get("how_this_combination", "Default interpretation"),
                "enjoyment": personality_data.get("what_you_might_enjoy", ["No enjoyment data available"]),
                "your_strength": personality_data.get("your_strength", ["No strength data available"]),
                "iconId": personality_data.get("icon_id", "1"),
                "riasecScores": riasec_scores
            },
            "industries": [
                {
                    "id": str(idx + 1),
                    "name": industry.get("industry", "Unknown Industry"),
                    "overview": industry.get("description", "No overview available"),
                    "trending": industry.get("trending", "No trending information available"),
                    "insight": industry.get("insight", "No insight available"),
                    "examplePaths": parse_career_paths(industry.get("career_path", [])),
                    "education": industry.get("education", ""),
                    "jupasInfo": parse_jupas_info(industry.get("education", ""))
                }
                for idx, industry in enumerate(unique_industries)
            ]
        }

        return analysis_result

    except Exception as e:
        import traceback
        traceback.print_exc()  # This will print the full stack trace
        raise HTTPException(
            status_code=500,
            detail=f"Error processing survey: {str(e)}"
        )

@router.get("/icon/{icon_id}")
async def get_icon(icon_id: str):
    try:
        # Updated path without double 'app'
        icon_dir = Path("static/icon")
        icon_path = icon_dir / f"{icon_id}.png"
        
        if not icon_path.exists():
            icon_path = icon_dir / "default.png"
            if not icon_path.exists():
                raise HTTPException(status_code=404, detail="Icon not found")
        
        return FileResponse(str(icon_path))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error serving icon: {str(e)}")

@router.get("/school-icon/{school}")
async def get_school_icon(school: str):
    try:
        # Updated path without double 'app'
        school_icon_dir = Path("static/school_icon")
        icon_path = school_icon_dir / f"{school}.png"
        
        if not icon_path.exists():
            icon_path = school_icon_dir / "default.png"
            if not icon_path.exists():
                raise HTTPException(status_code=404, detail="School icon not found")
        
        return FileResponse(str(icon_path))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error serving school icon: {str(e)}")
