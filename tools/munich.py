from langchain_core.tools import tool



@tool
def munich_advice(city: str)->bool:
    """ Returns a travel advice for munich"""
    return """Munich is a vibrant city in Germany known for its rich history, stunning architecture, and hosting DevOpsCon.
    It's a great place to explore on foot or by bike, with many museums, art galleries, and landmarks to visit.
    The city also has a lively nightlife scene, with bars, clubs, and restaurants to enjoy.
    Whether you're interested in art, history, or just want to relax and enjoy the city's atmosphere, Munich has something for everyone.
    """
