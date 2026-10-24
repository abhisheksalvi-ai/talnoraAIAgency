"""
Test suite for agent node implementations.
Uses pytest for async testing.
"""
import pytest
import json
from datetime import datetime
from unittest.mock import AsyncMock, patch, MagicMock

from app.agents.parsers import parse_job_description, JobStructure
from app.agents.scoring import score_candidates, filter_top_candidates, CandidateScore
from app.agents.outreach import draft_outreach_messages
from app.agents.embeddings import create_embedding, search_similar


class TestParsers:
    """Tests for job description parser"""
    
    @pytest.mark.asyncio
    async def test_parse_job_description(self):
        """Test parsing a job description"""
        mock_llm = AsyncMock()
        mock_llm.invoke.return_value = json.dumps({
            "title": "Senior DevOps Engineer",
            "description": "We are looking for a Senior DevOps Engineer...",
            "required_skills": ["Kubernetes", "AWS", "Terraform"],
            "nice_to_have_skills": ["Python", "Go"],
            "seniority": "senior",
            "experience_years_min": 5,
            "experience_years_max": 12,
            "location": "remote",
            "salary_range": {"min": 150000, "max": 200000},
            "job_type": "full-time"
        })
        
        result = await parse_job_description(
            "Senior DevOps Engineer job description...",
            "Senior DevOps Engineer",
            llm_client=mock_llm
        )
        
        assert isinstance(result, JobStructure)
        assert result.title == "Senior DevOps Engineer"
        assert "Kubernetes" in result.required_skills
        assert result.seniority == "senior"
        assert mock_llm.invoke.called
    
    @pytest.mark.asyncio
    async def test_parse_job_description_fallback(self):
        """Test parser fallback on LLM error"""
        mock_llm = AsyncMock()
        mock_llm.invoke.side_effect = Exception("LLM error")
        
        result = await parse_job_description(
            "Job description",
            "Job Title",
            llm_client=mock_llm
        )
        
        assert isinstance(result, JobStructure)
        assert result.title == "Job Title"


class TestScoring:
    """Tests for candidate scoring"""
    
    @pytest.mark.asyncio
    async def test_score_candidates(self):
        """Test candidate scoring"""
        mock_llm = AsyncMock()
        mock_llm.invoke.return_value = json.dumps([
            {
                "candidate_id": "cand1",
                "candidate_name": "John Doe",
                "score": 0.92,
                "skill_match": 0.95,
                "experience_match": 0.90,
                "location_match": 1.0,
                "seniority_match": 0.88,
                "gap_analysis": {"missing_skills": [], "nice_to_haves": ["Python"]},
                "reasoning": "Strong Kubernetes experience"
            }
        ])
        
        candidates = [
            {"id": "cand1", "name": "John Doe", "summary": "DevOps engineer"}
        ]
        job = {
            "title": "Senior DevOps",
            "required_skills": ["Kubernetes", "AWS"],
            "seniority": "senior",
            "experience_years_min": 5,
            "experience_years_max": 12
        }
        
        result = await score_candidates(candidates, job, llm_client=mock_llm)
        
        assert len(result.scored_candidates) == 1
        assert result.scored_candidates[0].score == 0.92
        assert result.scored_candidates[0].candidate_name == "John Doe"
    
    def test_filter_top_candidates(self):
        """Test candidate filtering"""
        candidates = [
            CandidateScore(candidate_id="1", candidate_name="A", score=0.95, skill_match=0.9, experience_match=0.9, location_match=1.0, seniority_match=0.9, reasoning="Good"),
            CandidateScore(candidate_id="2", candidate_name="B", score=0.80, skill_match=0.8, experience_match=0.8, location_match=1.0, seniority_match=0.8, reasoning="OK"),
            CandidateScore(candidate_id="3", candidate_name="C", score=0.65, skill_match=0.6, experience_match=0.7, location_match=0.6, seniority_match=0.6, reasoning="Below threshold"),
        ]
        
        filtered = filter_top_candidates(candidates, threshold=0.70, top_n=2)
        
        assert len(filtered) == 2
        assert filtered[0].candidate_id == "1"
        assert filtered[1].candidate_id == "2"


class TestEmbeddings:
    """Tests for embedding operations"""
    
    @pytest.mark.asyncio
    async def test_create_embedding(self):
        """Test embedding creation"""
        mock_embedding_client = AsyncMock()
        mock_embedding_client.embed.return_value = [0.1] * 1536
        
        result = await create_embedding(
            "Test text",
            embedding_client=mock_embedding_client
        )
        
        assert len(result.vector) == 1536
        assert result.dimension == 1536
        assert result.text_length == 9
    
    @pytest.mark.asyncio
    async def test_create_embedding_empty_text(self):
        """Test embedding with empty text"""
        mock_embedding_client = AsyncMock()
        
        result = await create_embedding(
            "",
            embedding_client=mock_embedding_client
        )
        
        assert result.text_length == 0
        assert len(result.vector) == 1536
