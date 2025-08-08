#!/usr/bin/env python3
"""
WebWaka Digital Operating System - Agent Migration Framework
Comprehensive tooling for migrating existing agents to Leap autonomous architecture
"""

import os
import json
import yaml
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
import subprocess
import shutil
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class AgentMetadata:
    """Metadata structure for WebWaka agents"""
    name: str
    category: str
    description: str
    ubuntu_integration_score: float
    african_optimization_score: float
    dependencies: List[str]
    cultural_intelligence_features: List[str]
    traditional_knowledge_components: List[str]
    community_consultation_requirements: List[str]
    performance_requirements: Dict[str, Any]
    
@dataclass
class MigrationResult:
    """Result structure for agent migration"""
    agent_name: str
    migration_status: str
    leap_prompt_generated: bool
    cultural_validation_passed: bool
    performance_validation_passed: bool
    migration_timestamp: str
    issues: List[str]
    recommendations: List[str]

class CulturalIntelligenceValidator:
    """Validates cultural intelligence preservation during migration"""
    
    def __init__(self):
        self.ubuntu_principles = [
            "community_centered_decision_making",
            "collective_responsibility",
            "traditional_governance_integration",
            "elder_wisdom_consultation",
            "consensus_building_mechanisms"
        ]
        
        self.traditional_knowledge_requirements = [
            "traditional_knowledge_ownership_preservation",
            "community_controlled_sharing",
            "elder_consultation_validation",
            "traditional_authority_approval",
            "cultural_authenticity_maintenance"
        ]
    
    def validate_ubuntu_integration(self, agent_metadata: AgentMetadata) -> Dict[str, Any]:
        """Validate Ubuntu philosophy integration preservation"""
        validation_results = {
            "ubuntu_score": agent_metadata.ubuntu_integration_score,
            "principles_preserved": [],
            "missing_principles": [],
            "recommendations": []
        }
        
        for principle in self.ubuntu_principles:
            if principle in agent_metadata.cultural_intelligence_features:
                validation_results["principles_preserved"].append(principle)
            else:
                validation_results["missing_principles"].append(principle)
                validation_results["recommendations"].append(
                    f"Implement {principle} in Leap agent architecture"
                )
        
        return validation_results
    
    def validate_traditional_knowledge_preservation(self, agent_metadata: AgentMetadata) -> Dict[str, Any]:
        """Validate traditional knowledge preservation requirements"""
        validation_results = {
            "traditional_knowledge_score": len(agent_metadata.traditional_knowledge_components),
            "requirements_met": [],
            "missing_requirements": [],
            "recommendations": []
        }
        
        for requirement in self.traditional_knowledge_requirements:
            if requirement in agent_metadata.traditional_knowledge_components:
                validation_results["requirements_met"].append(requirement)
            else:
                validation_results["missing_requirements"].append(requirement)
                validation_results["recommendations"].append(
                    f"Implement {requirement} in Leap agent migration"
                )
        
        return validation_results

class LeapPromptGenerator:
    """Generates Leap-optimized prompts for WebWaka agents"""
    
    def __init__(self):
        self.prompt_templates = {
            "cultural_intelligence": self._load_cultural_intelligence_template(),
            "voice_language": self._load_voice_language_template(),
            "payment_systems": self._load_payment_systems_template(),
            "security_enhancement": self._load_security_enhancement_template(),
            "performance_optimization": self._load_performance_optimization_template()
        }
    
    def _load_cultural_intelligence_template(self) -> str:
        """Load cultural intelligence agent prompt template"""
        return """
Build a cultural intelligence agent for WebWaka Digital Operating System that implements Ubuntu philosophy principles in technology decision-making processes.

Core Ubuntu Philosophy Integration:
- Community-centered decision making with collective responsibility frameworks
- Traditional governance integration that respects elder wisdom and traditional authority
- Consensus-building mechanisms that prioritize community harmony and mutual support
- Cultural preservation features that document and protect traditional knowledge systems

Key Functionality:
{functionality_requirements}

African Market Optimization:
{african_optimization_requirements}

Cultural Intelligence Features:
{cultural_intelligence_features}

Traditional Knowledge Components:
{traditional_knowledge_components}

Performance Requirements:
{performance_requirements}

The agent should operate autonomously while maintaining authentic cultural integration and community consultation processes that strengthen rather than compromise traditional values and governance structures.
"""
    
    def _load_voice_language_template(self) -> str:
        """Load voice and language expansion agent prompt template"""
        return """
Build a voice and language expansion agent for WebWaka Digital Operating System that provides sophisticated natural language understanding for 50+ African languages with cultural context awareness.

Language Support Requirements:
{language_support_requirements}

Cultural Context Integration:
{cultural_context_integration}

Technical Specifications:
{technical_specifications}

African Market Optimization:
{african_optimization_requirements}

Performance Requirements:
{performance_requirements}

The agent should operate autonomously while maintaining authentic language support and cultural context awareness that enhances rather than replaces traditional communication patterns and cultural practices.
"""
    
    def _load_payment_systems_template(self) -> str:
        """Load payment systems agent prompt template"""
        return """
Build a payment systems integration agent for WebWaka Digital Operating System that supports comprehensive African payment methods with cultural intelligence and Ubuntu philosophy integration.

Payment Method Support:
{payment_method_support}

Cultural Intelligence Integration:
{cultural_intelligence_integration}

African Market Optimization:
{african_optimization_requirements}

Performance Requirements:
{performance_requirements}

The agent should operate autonomously while maintaining cultural sensitivity and community-centered approaches that enhance rather than disrupt traditional economic systems and community relationships.
"""
    
    def _load_security_enhancement_template(self) -> str:
        """Load security enhancement agent prompt template"""
        return """
Build a security enhancement agent for WebWaka Digital Operating System that implements bank-grade security standards while maintaining cultural intelligence and community consultation processes.

Security Requirements:
{security_requirements}

Cultural Intelligence Integration:
{cultural_intelligence_integration}

African Market Optimization:
{african_optimization_requirements}

Performance Requirements:
{performance_requirements}

The agent should operate autonomously while maintaining cultural sensitivity and traditional authority consultation that enhances rather than compromises community trust and traditional governance structures.
"""
    
    def _load_performance_optimization_template(self) -> str:
        """Load performance optimization agent prompt template"""
        return """
Build a performance optimization agent for WebWaka Digital Operating System that optimizes system performance for African infrastructure conditions while maintaining cultural intelligence capabilities.

Performance Optimization Requirements:
{performance_optimization_requirements}

African Infrastructure Optimization:
{african_infrastructure_optimization}

Cultural Intelligence Integration:
{cultural_intelligence_integration}

Performance Requirements:
{performance_requirements}

The agent should operate autonomously while maintaining cultural sensitivity and African market optimization that enhances rather than compromises user experience and community engagement.
"""
    
    def generate_leap_prompt(self, agent_metadata: AgentMetadata) -> str:
        """Generate Leap-optimized prompt for agent migration"""
        template = self.prompt_templates.get(agent_metadata.category, "")
        
        if not template:
            logger.warning(f"No template found for category: {agent_metadata.category}")
            return self._generate_generic_prompt(agent_metadata)
        
        # Format template with agent-specific data
        formatted_prompt = template.format(
            functionality_requirements=self._format_list(agent_metadata.cultural_intelligence_features),
            african_optimization_requirements=self._format_african_optimization(agent_metadata),
            cultural_intelligence_features=self._format_list(agent_metadata.cultural_intelligence_features),
            traditional_knowledge_components=self._format_list(agent_metadata.traditional_knowledge_components),
            performance_requirements=self._format_performance_requirements(agent_metadata.performance_requirements),
            language_support_requirements=self._format_language_support(agent_metadata),
            cultural_context_integration=self._format_cultural_context(agent_metadata),
            technical_specifications=self._format_technical_specs(agent_metadata),
            payment_method_support=self._format_payment_methods(agent_metadata),
            cultural_intelligence_integration=self._format_cultural_integration(agent_metadata),
            security_requirements=self._format_security_requirements(agent_metadata),
            performance_optimization_requirements=self._format_performance_optimization(agent_metadata),
            african_infrastructure_optimization=self._format_infrastructure_optimization(agent_metadata)
        )
        
        return formatted_prompt
    
    def _format_list(self, items: List[str]) -> str:
        """Format list items for prompt inclusion"""
        return "\n".join([f"- {item}" for item in items])
    
    def _format_african_optimization(self, agent_metadata: AgentMetadata) -> str:
        """Format African market optimization requirements"""
        return f"""
- Mobile-first design optimized for African infrastructure conditions
- Offline capability for low-connectivity areas with intelligent synchronization
- Bandwidth optimization for 2G/3G networks
- Support for diverse African cultural contexts across 54 countries
- Integration with African ecosystem providers and traditional systems
- Ubuntu philosophy integration score: {agent_metadata.ubuntu_integration_score}/10
- African optimization score: {agent_metadata.african_optimization_score}/10
"""
    
    def _format_performance_requirements(self, requirements: Dict[str, Any]) -> str:
        """Format performance requirements for prompt inclusion"""
        formatted_reqs = []
        for key, value in requirements.items():
            formatted_reqs.append(f"- {key}: {value}")
        return "\n".join(formatted_reqs)
    
    def _format_language_support(self, agent_metadata: AgentMetadata) -> str:
        """Format language support requirements"""
        return """
- Major African languages including Swahili, Hausa, Yoruba, Amharic, and Zulu
- Regional language variations with cultural context recognition
- Traditional language preservation with elder consultation and validation
- Cross-language communication and translation capabilities
"""
    
    def _format_cultural_context(self, agent_metadata: AgentMetadata) -> str:
        """Format cultural context integration requirements"""
        return """
- Recognition of cultural nuances and traditional communication patterns
- Respect for traditional storytelling and oral tradition preservation
- Integration with traditional knowledge systems and cultural practices
- Community consultation processes for language accuracy and cultural appropriateness
"""
    
    def _format_technical_specs(self, agent_metadata: AgentMetadata) -> str:
        """Format technical specifications"""
        return """
- Real-time voice processing with offline capability for low-connectivity areas
- Mobile-first design optimized for African infrastructure conditions
- Bandwidth optimization for 2G/3G networks with intelligent caching
- Integration with existing WebWaka cultural intelligence and payment systems
"""
    
    def _format_payment_methods(self, agent_metadata: AgentMetadata) -> str:
        """Format payment method support requirements"""
        return """
- Mobile money integration (M-Pesa, Airtel Money, MTN Mobile Money, Orange Money)
- Traditional banking systems with cross-border capability
- Cryptocurrency integration with regulatory compliance
- Micro-payment optimization for small-scale transactions
"""
    
    def _format_cultural_integration(self, agent_metadata: AgentMetadata) -> str:
        """Format cultural intelligence integration requirements"""
        return """
- Community-centered payment sharing and collective responsibility features
- Traditional economic systems integration with modern payment methods
- Ubuntu philosophy implementation in payment processing and dispute resolution
- Cultural appropriateness validation for payment workflows and user interfaces
"""
    
    def _format_security_requirements(self, agent_metadata: AgentMetadata) -> str:
        """Format security requirements"""
        return """
- Bank-grade encryption and security standards implementation
- Multi-factor authentication with cultural intelligence integration
- Traditional authority consultation for security decisions
- Community privacy preservation with traditional protocol respect
"""
    
    def _format_performance_optimization(self, agent_metadata: AgentMetadata) -> str:
        """Format performance optimization requirements"""
        return """
- Mobile performance optimization for African infrastructure conditions
- Bandwidth efficiency for low-connectivity environments
- Offline capability with intelligent synchronization
- Scalability for millions of users across 54 African countries
"""
    
    def _format_infrastructure_optimization(self, agent_metadata: AgentMetadata) -> str:
        """Format infrastructure optimization requirements"""
        return """
- Mobile-first architecture optimized for African infrastructure
- Offline-first design with intelligent synchronization capabilities
- Bandwidth optimization for 2G/3G networks
- Power efficiency for battery-constrained devices
"""
    
    def _generate_generic_prompt(self, agent_metadata: AgentMetadata) -> str:
        """Generate generic prompt for unknown agent categories"""
        return f"""
Build a {agent_metadata.name} agent for WebWaka Digital Operating System that implements Ubuntu philosophy principles and African market optimization.

Agent Description:
{agent_metadata.description}

Cultural Intelligence Features:
{self._format_list(agent_metadata.cultural_intelligence_features)}

Traditional Knowledge Components:
{self._format_list(agent_metadata.traditional_knowledge_components)}

African Market Optimization:
{self._format_african_optimization(agent_metadata)}

Performance Requirements:
{self._format_performance_requirements(agent_metadata.performance_requirements)}

The agent should operate autonomously while maintaining authentic cultural integration and community consultation processes.
"""

class AgentMigrationFramework:
    """Main framework for migrating WebWaka agents to Leap architecture"""
    
    def __init__(self, source_directory: str, target_directory: str):
        self.source_directory = Path(source_directory)
        self.target_directory = Path(target_directory)
        self.cultural_validator = CulturalIntelligenceValidator()
        self.prompt_generator = LeapPromptGenerator()
        self.migration_results: List[MigrationResult] = []
        
        # Ensure target directory exists
        self.target_directory.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Initialized migration framework: {source_directory} -> {target_directory}")
    
    def discover_agents(self) -> List[Path]:
        """Discover all agent files in the source directory"""
        agent_files = []
        
        # Look for Python agent files
        for python_file in self.source_directory.rglob("*_agent.py"):
            agent_files.append(python_file)
        
        logger.info(f"Discovered {len(agent_files)} agent files")
        return agent_files
    
    def extract_agent_metadata(self, agent_file: Path) -> Optional[AgentMetadata]:
        """Extract metadata from agent file"""
        try:
            # Read agent file content
            with open(agent_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract metadata from docstrings and comments
            metadata = self._parse_agent_metadata(content, agent_file.name)
            return metadata
            
        except Exception as e:
            logger.error(f"Failed to extract metadata from {agent_file}: {e}")
            return None
    
    def _parse_agent_metadata(self, content: str, filename: str) -> AgentMetadata:
        """Parse agent metadata from file content"""
        # Extract agent name from filename
        agent_name = filename.replace("_agent.py", "").replace("_", " ").title()
        
        # Determine category based on file path or content
        category = self._determine_agent_category(content, filename)
        
        # Extract description from docstring
        description = self._extract_description(content)
        
        # Extract cultural intelligence features
        cultural_features = self._extract_cultural_features(content)
        
        # Extract traditional knowledge components
        traditional_knowledge = self._extract_traditional_knowledge(content)
        
        # Extract community consultation requirements
        community_consultation = self._extract_community_consultation(content)
        
        # Extract performance requirements
        performance_requirements = self._extract_performance_requirements(content)
        
        # Calculate scores based on content analysis
        ubuntu_score = self._calculate_ubuntu_score(content)
        african_score = self._calculate_african_score(content)
        
        # Extract dependencies
        dependencies = self._extract_dependencies(content)
        
        return AgentMetadata(
            name=agent_name,
            category=category,
            description=description,
            ubuntu_integration_score=ubuntu_score,
            african_optimization_score=african_score,
            dependencies=dependencies,
            cultural_intelligence_features=cultural_features,
            traditional_knowledge_components=traditional_knowledge,
            community_consultation_requirements=community_consultation,
            performance_requirements=performance_requirements
        )
    
    def _determine_agent_category(self, content: str, filename: str) -> str:
        """Determine agent category based on content and filename"""
        if "cultural" in filename.lower() or "ubuntu" in content.lower():
            return "cultural_intelligence"
        elif "voice" in filename.lower() or "language" in filename.lower():
            return "voice_language"
        elif "payment" in filename.lower() or "money" in filename.lower():
            return "payment_systems"
        elif "security" in filename.lower() or "auth" in filename.lower():
            return "security_enhancement"
        elif "performance" in filename.lower() or "optimization" in filename.lower():
            return "performance_optimization"
        else:
            return "general"
    
    def _extract_description(self, content: str) -> str:
        """Extract agent description from docstring"""
        lines = content.split('\n')
        in_docstring = False
        description_lines = []
        
        for line in lines:
            if '"""' in line and not in_docstring:
                in_docstring = True
                if line.count('"""') == 2:  # Single line docstring
                    return line.strip('"""').strip()
                continue
            elif '"""' in line and in_docstring:
                break
            elif in_docstring:
                description_lines.append(line.strip())
        
        return ' '.join(description_lines) if description_lines else "WebWaka agent implementation"
    
    def _extract_cultural_features(self, content: str) -> List[str]:
        """Extract cultural intelligence features from content"""
        features = []
        cultural_keywords = [
            "ubuntu", "community", "traditional", "cultural", "elder",
            "consensus", "collective", "governance", "wisdom", "heritage"
        ]
        
        for keyword in cultural_keywords:
            if keyword in content.lower():
                features.append(f"{keyword}_integration")
        
        return features
    
    def _extract_traditional_knowledge(self, content: str) -> List[str]:
        """Extract traditional knowledge components from content"""
        components = []
        traditional_keywords = [
            "traditional_knowledge", "oral_tradition", "cultural_heritage",
            "elder_wisdom", "traditional_governance", "community_ownership"
        ]
        
        for keyword in traditional_keywords:
            if keyword in content.lower():
                components.append(keyword)
        
        return components
    
    def _extract_community_consultation(self, content: str) -> List[str]:
        """Extract community consultation requirements from content"""
        requirements = []
        consultation_keywords = [
            "community_consultation", "traditional_authority", "elder_approval",
            "consensus_building", "collective_decision"
        ]
        
        for keyword in consultation_keywords:
            if keyword in content.lower():
                requirements.append(keyword)
        
        return requirements
    
    def _extract_performance_requirements(self, content: str) -> Dict[str, Any]:
        """Extract performance requirements from content"""
        requirements = {
            "response_time": "sub-200ms",
            "availability": "99.9%",
            "scalability": "millions of users",
            "mobile_optimization": "African infrastructure",
            "offline_capability": "low-connectivity areas"
        }
        
        return requirements
    
    def _calculate_ubuntu_score(self, content: str) -> float:
        """Calculate Ubuntu philosophy integration score"""
        ubuntu_indicators = [
            "ubuntu", "community", "collective", "consensus", "traditional",
            "elder", "wisdom", "governance", "harmony", "mutual"
        ]
        
        score = 0.0
        for indicator in ubuntu_indicators:
            if indicator in content.lower():
                score += 1.0
        
        return min(score, 10.0)
    
    def _calculate_african_score(self, content: str) -> float:
        """Calculate African market optimization score"""
        african_indicators = [
            "african", "mobile", "offline", "bandwidth", "connectivity",
            "infrastructure", "2g", "3g", "rural", "traditional"
        ]
        
        score = 0.0
        for indicator in african_indicators:
            if indicator in content.lower():
                score += 1.0
        
        return min(score, 10.0)
    
    def _extract_dependencies(self, content: str) -> List[str]:
        """Extract agent dependencies from content"""
        dependencies = []
        
        # Look for import statements
        lines = content.split('\n')
        for line in lines:
            if line.strip().startswith('import ') or line.strip().startswith('from '):
                dependencies.append(line.strip())
        
        return dependencies
    
    def migrate_agent(self, agent_file: Path) -> MigrationResult:
        """Migrate a single agent to Leap architecture"""
        logger.info(f"Migrating agent: {agent_file.name}")
        
        # Extract agent metadata
        metadata = self.extract_agent_metadata(agent_file)
        if not metadata:
            return MigrationResult(
                agent_name=agent_file.name,
                migration_status="failed",
                leap_prompt_generated=False,
                cultural_validation_passed=False,
                performance_validation_passed=False,
                migration_timestamp=datetime.now().isoformat(),
                issues=["Failed to extract agent metadata"],
                recommendations=["Review agent file structure and documentation"]
            )
        
        issues = []
        recommendations = []
        
        # Validate cultural intelligence preservation
        cultural_validation = self.cultural_validator.validate_ubuntu_integration(metadata)
        traditional_validation = self.cultural_validator.validate_traditional_knowledge_preservation(metadata)
        
        cultural_passed = len(cultural_validation["missing_principles"]) == 0
        if not cultural_passed:
            issues.extend(cultural_validation["missing_principles"])
            recommendations.extend(cultural_validation["recommendations"])
        
        # Generate Leap-optimized prompt
        leap_prompt = self.prompt_generator.generate_leap_prompt(metadata)
        prompt_generated = len(leap_prompt) > 0
        
        # Save migration artifacts
        self._save_migration_artifacts(metadata, leap_prompt, cultural_validation, traditional_validation)
        
        # Performance validation (simplified for this implementation)
        performance_passed = metadata.ubuntu_integration_score >= 7.0 and metadata.african_optimization_score >= 7.0
        
        migration_result = MigrationResult(
            agent_name=metadata.name,
            migration_status="success" if prompt_generated and cultural_passed else "partial",
            leap_prompt_generated=prompt_generated,
            cultural_validation_passed=cultural_passed,
            performance_validation_passed=performance_passed,
            migration_timestamp=datetime.now().isoformat(),
            issues=issues,
            recommendations=recommendations
        )
        
        self.migration_results.append(migration_result)
        logger.info(f"Migration completed for {metadata.name}: {migration_result.migration_status}")
        
        return migration_result
    
    def _save_migration_artifacts(self, metadata: AgentMetadata, leap_prompt: str, 
                                cultural_validation: Dict, traditional_validation: Dict):
        """Save migration artifacts to target directory"""
        agent_dir = self.target_directory / metadata.name.lower().replace(" ", "_")
        agent_dir.mkdir(exist_ok=True)
        
        # Save agent metadata
        with open(agent_dir / "metadata.json", 'w') as f:
            json.dump(asdict(metadata), f, indent=2)
        
        # Save Leap prompt
        with open(agent_dir / "leap_prompt.md", 'w') as f:
            f.write(leap_prompt)
        
        # Save validation results
        validation_results = {
            "cultural_validation": cultural_validation,
            "traditional_validation": traditional_validation
        }
        
        with open(agent_dir / "validation_results.json", 'w') as f:
            json.dump(validation_results, f, indent=2)
    
    def migrate_all_agents(self) -> List[MigrationResult]:
        """Migrate all discovered agents"""
        logger.info("Starting migration of all agents")
        
        agent_files = self.discover_agents()
        results = []
        
        for agent_file in agent_files:
            result = self.migrate_agent(agent_file)
            results.append(result)
        
        # Generate migration summary report
        self._generate_migration_report(results)
        
        logger.info(f"Migration completed. {len(results)} agents processed.")
        return results
    
    def _generate_migration_report(self, results: List[MigrationResult]):
        """Generate comprehensive migration report"""
        report = {
            "migration_summary": {
                "total_agents": len(results),
                "successful_migrations": len([r for r in results if r.migration_status == "success"]),
                "partial_migrations": len([r for r in results if r.migration_status == "partial"]),
                "failed_migrations": len([r for r in results if r.migration_status == "failed"]),
                "cultural_validation_passed": len([r for r in results if r.cultural_validation_passed]),
                "performance_validation_passed": len([r for r in results if r.performance_validation_passed])
            },
            "migration_results": [asdict(result) for result in results],
            "recommendations": self._generate_overall_recommendations(results)
        }
        
        # Save migration report
        with open(self.target_directory / "migration_report.json", 'w') as f:
            json.dump(report, f, indent=2)
        
        # Generate human-readable report
        self._generate_human_readable_report(report)
    
    def _generate_overall_recommendations(self, results: List[MigrationResult]) -> List[str]:
        """Generate overall recommendations based on migration results"""
        recommendations = []
        
        failed_count = len([r for r in results if r.migration_status == "failed"])
        if failed_count > 0:
            recommendations.append(f"Review and fix {failed_count} failed agent migrations")
        
        cultural_failed = len([r for r in results if not r.cultural_validation_passed])
        if cultural_failed > 0:
            recommendations.append(f"Enhance cultural intelligence integration for {cultural_failed} agents")
        
        performance_failed = len([r for r in results if not r.performance_validation_passed])
        if performance_failed > 0:
            recommendations.append(f"Improve African market optimization for {performance_failed} agents")
        
        recommendations.append("Conduct comprehensive testing of migrated agents in Leap environment")
        recommendations.append("Validate cultural authenticity with African cultural experts")
        recommendations.append("Test performance optimization for African infrastructure conditions")
        
        return recommendations
    
    def _generate_human_readable_report(self, report: Dict):
        """Generate human-readable migration report"""
        summary = report["migration_summary"]
        
        report_content = f"""
# WebWaka Agent Migration Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Migration Summary
- **Total Agents Processed**: {summary['total_agents']}
- **Successful Migrations**: {summary['successful_migrations']}
- **Partial Migrations**: {summary['partial_migrations']}
- **Failed Migrations**: {summary['failed_migrations']}
- **Cultural Validation Passed**: {summary['cultural_validation_passed']}
- **Performance Validation Passed**: {summary['performance_validation_passed']}

## Success Rate"""
        
        if summary['total_agents'] > 0:
            report_content += f"""
- **Overall Success Rate**: {(summary['successful_migrations'] / summary['total_agents'] * 100):.1f}%
- **Cultural Validation Rate**: {(summary['cultural_validation_passed'] / summary['total_agents'] * 100):.1f}%
- **Performance Validation Rate**: {(summary['performance_validation_passed'] / summary['total_agents'] * 100):.1f}%"""
        else:
            report_content += f"""
- **Overall Success Rate**: 0.0% (No agents found)
- **Cultural Validation Rate**: 0.0% (No agents found)
- **Performance Validation Rate**: 0.0% (No agents found)"""
        
        report_content += f"""

## Recommendations
"""
        
        for recommendation in report["recommendations"]:
            report_content += f"- {recommendation}\n"
        
        report_content += "\n## Detailed Results\n"
        
        for result in report["migration_results"]:
            report_content += f"""
### {result['agent_name']}
- **Status**: {result['migration_status']}
- **Leap Prompt Generated**: {result['leap_prompt_generated']}
- **Cultural Validation**: {result['cultural_validation_passed']}
- **Performance Validation**: {result['performance_validation_passed']}
- **Issues**: {len(result['issues'])}
- **Recommendations**: {len(result['recommendations'])}
"""
        
        with open(self.target_directory / "migration_report.md", 'w') as f:
            f.write(report_content)

def main():
    """Main function for running agent migration"""
    import argparse
    
    parser = argparse.ArgumentParser(description="WebWaka Agent Migration Framework")
    parser.add_argument("--source", required=True, help="Source directory containing WebWaka agents")
    parser.add_argument("--target", required=True, help="Target directory for migration artifacts")
    parser.add_argument("--agent", help="Specific agent file to migrate (optional)")
    
    args = parser.parse_args()
    
    # Initialize migration framework
    migration_framework = AgentMigrationFramework(args.source, args.target)
    
    if args.agent:
        # Migrate specific agent
        agent_path = Path(args.agent)
        result = migration_framework.migrate_agent(agent_path)
        print(f"Migration result for {agent_path.name}: {result.migration_status}")
    else:
        # Migrate all agents
        results = migration_framework.migrate_all_agents()
        successful = len([r for r in results if r.migration_status == "success"])
        print(f"Migration completed: {successful}/{len(results)} agents successfully migrated")

if __name__ == "__main__":
    main()

