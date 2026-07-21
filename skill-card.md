## Description: <br>
Travel Guide Generator helps users create multilingual, responsive HTML travel guides with daily itineraries, route timing, hotel and food recommendations, budget estimates, and practical travel tips. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gmmg55](https://clawhub.ai/user/gmmg55) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel planners use this skill to turn destination, duration, departure city, and style preferences into a detailed travel guide. It is intended for itinerary planning, route estimation, hotel and food recommendations, avoid-list guidance, and shareable HTML output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Travel details may be sent to external search services and Amap during guide generation. <br>
Mitigation: Review whether the destination, route, and itinerary details are appropriate to share with those services before using live lookups. <br>
Risk: The skill can require a sensitive Amap API key for route calculations. <br>
Mitigation: Provide the key through a scoped, revocable environment variable or secret manager, avoid pasting it into chat, and rotate any key that was exposed. <br>
Risk: Generated travel recommendations, prices, schedules, and route timing can be incomplete or outdated. <br>
Mitigation: Verify important reservations, opening hours, transportation options, and safety-sensitive travel details against authoritative current sources before relying on the guide. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/gmmg55/travel-guide-generator) <br>
- [README](README.md) <br>
- [Daily Itinerary Specification](references/daily-itinerary-spec.md) <br>
- [Design Specification](references/design-spec.md) <br>
- [Amap Web Service API](https://lbs.amap.com/) <br>
- [Amap Driving Route API](https://restapi.amap.com/v3/direction/driving) <br>
- [Amap Distance API](https://restapi.amap.com/v3/distance) <br>
- [Amap POI Search API](https://restapi.amap.com/v3/place/text) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Responsive HTML file plus Markdown or text itinerary summary; helper scripts may emit JSON route or search-query data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use an optional AMAP_KEY environment variable for Amap route calculations; without it, route details may rely on estimates or other available sources.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
