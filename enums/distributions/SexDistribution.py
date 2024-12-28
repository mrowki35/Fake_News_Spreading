from enums.groups.SexGroup import SexGroup
from enums.SocialPlatform import SocialPlatform

SexDistribution = {
    SocialPlatform.LinkedIn: {
        SexGroup.MALE: 0.55,
        SexGroup.FEMALE: 0.40,
        SexGroup.OTHER: 0.05,
    },
    SocialPlatform.Facebook: {
        SexGroup.MALE: 0.48,
        SexGroup.FEMALE: 0.48,
        SexGroup.OTHER: 0.04,
    },
    SocialPlatform.Instagram: {
        SexGroup.MALE: 0.45,
        SexGroup.FEMALE: 0.50,
        SexGroup.OTHER: 0.05,
    },
    SocialPlatform.X: {
        SexGroup.MALE: 0.50,
        SexGroup.FEMALE: 0.45,
        SexGroup.OTHER: 0.05,
    },
    SocialPlatform.Telegram: {
        SexGroup.MALE: 0.52,
        SexGroup.FEMALE: 0.43,
        SexGroup.OTHER: 0.05,
    },
    SocialPlatform.Reddit: {
        SexGroup.MALE: 0.60,
        SexGroup.FEMALE: 0.35,
        SexGroup.OTHER: 0.05,
    },
    SocialPlatform.Pinterest: {
        SexGroup.MALE: 0.30,
        SexGroup.FEMALE: 0.65,
        SexGroup.OTHER: 0.05,
    },
    SocialPlatform.Snapchat: {
        SexGroup.MALE: 0.40,
        SexGroup.FEMALE: 0.55,
        SexGroup.OTHER: 0.05,
    },
    SocialPlatform.TikTok: {
        SexGroup.MALE: 0.47,
        SexGroup.FEMALE: 0.48,
        SexGroup.OTHER: 0.05,
    },
    SocialPlatform.YouTube: {
        SexGroup.MALE: 0.50,
        SexGroup.FEMALE: 0.45,
        SexGroup.OTHER: 0.05,
    },
    SocialPlatform.WeChat: {
        SexGroup.MALE: 0.51,
        SexGroup.FEMALE: 0.45,
        SexGroup.OTHER: 0.04,
    },
    SocialPlatform.Weibo: {
        SexGroup.MALE: 0.52,
        SexGroup.FEMALE: 0.43,
        SexGroup.OTHER: 0.05,
    },
    SocialPlatform.Other: {
        SexGroup.MALE: 0.49,
        SexGroup.FEMALE: 0.47,
        SexGroup.OTHER: 0.04,
    },
}

for platform, distribution in SexDistribution.items():
    total = sum(distribution.values())
    if not abs(total - 1.0) < 1e-6:
        raise ValueError(f"Sex distribution for {platform.name} does not sum to 1.0 (sum={total})")
