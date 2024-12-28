from enums.groups.EducationGroup import EducationGroup
from enums.SocialPlatform import SocialPlatform

EducationDistribution = {
    SocialPlatform.LinkedIn: {
        EducationGroup.PRIMARY: 0.02,
        EducationGroup.SECONDARY: 0.18,
        EducationGroup.HIGHER: 0.75,
        EducationGroup.VOCATIONAL: 0.05,
    },
    SocialPlatform.Facebook: {
        EducationGroup.PRIMARY: 0.10,
        EducationGroup.SECONDARY: 0.40,
        EducationGroup.HIGHER: 0.45,
        EducationGroup.VOCATIONAL: 0.05,
    },
    SocialPlatform.Instagram: {
        EducationGroup.PRIMARY: 0.05,
        EducationGroup.SECONDARY: 0.30,
        EducationGroup.HIGHER: 0.60,
        EducationGroup.VOCATIONAL: 0.05,
    },
    SocialPlatform.X: {
        EducationGroup.PRIMARY: 0.03,
        EducationGroup.SECONDARY: 0.27,
        EducationGroup.HIGHER: 0.65,
        EducationGroup.VOCATIONAL: 0.05,
    },
    SocialPlatform.Telegram: {
        EducationGroup.PRIMARY: 0.04,
        EducationGroup.SECONDARY: 0.35,
        EducationGroup.HIGHER: 0.55,
        EducationGroup.VOCATIONAL: 0.06,
    },
    SocialPlatform.Reddit: {
        EducationGroup.PRIMARY: 0.01,
        EducationGroup.SECONDARY: 0.20,
        EducationGroup.HIGHER: 0.75,
        EducationGroup.VOCATIONAL: 0.04,
    },
    SocialPlatform.Pinterest: {
        EducationGroup.PRIMARY: 0.03,
        EducationGroup.SECONDARY: 0.22,
        EducationGroup.HIGHER: 0.70,
        EducationGroup.VOCATIONAL: 0.05,
    },
    SocialPlatform.Snapchat: {
        EducationGroup.PRIMARY: 0.08,
        EducationGroup.SECONDARY: 0.25,
        EducationGroup.HIGHER: 0.60,
        EducationGroup.VOCATIONAL: 0.07,
    },
    SocialPlatform.TikTok: {
        EducationGroup.PRIMARY: 0.25,
        EducationGroup.SECONDARY: 0.50,
        EducationGroup.HIGHER: 0.20,
        EducationGroup.VOCATIONAL: 0.05,
    },
    SocialPlatform.YouTube: {
        EducationGroup.PRIMARY: 0.05,
        EducationGroup.SECONDARY: 0.25,
        EducationGroup.HIGHER: 0.65,
        EducationGroup.VOCATIONAL: 0.05,
    },
    SocialPlatform.WeChat: {
        EducationGroup.PRIMARY: 0.04,
        EducationGroup.SECONDARY: 0.30,
        EducationGroup.HIGHER: 0.60,
        EducationGroup.VOCATIONAL: 0.06,
    },
    SocialPlatform.Weibo: {
        EducationGroup.PRIMARY: 0.03,
        EducationGroup.SECONDARY: 0.28,
        EducationGroup.HIGHER: 0.65,
        EducationGroup.VOCATIONAL: 0.04,
    },
    SocialPlatform.Other: {
        EducationGroup.PRIMARY: 0.05,
        EducationGroup.SECONDARY: 0.25,
        EducationGroup.HIGHER: 0.65,
        EducationGroup.VOCATIONAL: 0.05,
    },
}

for platform, distribution in EducationDistribution.items():
    total = sum(distribution.values())
    if not abs(total - 1.0) < 1e-6:
        raise ValueError(f"Education distribution for {platform.name} does not sum to 1.0 (sum={total})")
