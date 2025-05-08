def colorize_markdown(md):
    """Colorize markdown text with emoji indicators.
    
    Args:
        md (str): Markdown text containing emoji indicators
        
    Returns:
        str: HTML with colored emoji indicators
    """
    md = md.replace("🟢", '<span style="color:#34d399;font-weight:700;">🟢</span>')
    md = md.replace("🟡", '<span style="color:#fbbf24;font-weight:700;">🟡</span>')
    md = md.replace("🔴", '<span style="color:#f87171;font-weight:700;">🔴</span>')
    return md 