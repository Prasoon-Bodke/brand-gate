#!/usr/bin/env python3
"""
Seed database with sample guidelines, facts, and assets from datasets/ directory.
"""
import os
import sys
import json
import asyncio
from pathlib import Path

# Add backend directory to path
sys.path.append(str(Path(__file__).parent.parent / "backend"))

from app.core.database import AsyncSessionLocal
from app.models.brand import BrandGuideline, ApprovedFact, BrandAsset


async def seed_data():
    """Load sample JSON data into database."""
    base_dir = Path(__file__).parent.parent / "datasets"

    print("Starting database seed process...")

    async with AsyncSessionLocal() as session:
        # Seed Terminology Rules
        terminology_file = base_dir / "brand_guidelines" / "terminology_rules.json"
        if terminology_file.exists():
            with open(terminology_file) as f:
                data = json.load(f)
                for item in data.get("guidelines", []):
                    guideline = BrandGuideline(
                        name=item["name"],
                        description=item["description"],
                        category=item["category"],
                        rule_text=json.dumps(item),
                        rule_type=item["rule_type"],
                        severity=item["severity"],
                        is_active=True
                    )
                    session.add(guideline)
            print("Loaded terminology rules")

        # Seed Visual Rules
        visual_file = base_dir / "brand_guidelines" / "visual_rules.json"
        if visual_file.exists():
            with open(visual_file) as f:
                data = json.load(f)
                for item in data.get("guidelines", []):
                    guideline = BrandGuideline(
                        name=item["name"],
                        description=item["description"],
                        category=item["category"],
                        rule_text=json.dumps(item),
                        rule_type=item["rule_type"],
                        severity=item["severity"],
                        is_active=True
                    )
                    session.add(guideline)
            print("Loaded visual rules")

        # Seed Approved Facts
        claims_file = base_dir / "approved_facts" / "claims.json"
        if claims_file.exists():
            with open(claims_file) as f:
                data = json.load(f)
                for item in data.get("facts", []):
                    fact = ApprovedFact(
                        fact_text=item["fact_text"],
                        fact_type=item["fact_type"],
                        source_url=item.get("source_url"),
                        tags=item.get("tags", []),
                        is_active=True
                    )
                    session.add(fact)
            print("Loaded approved facts")

        await session.commit()
        print("Database seed completed successfully!")


if __name__ == "__main__":
    asyncio.run(seed_data())