import re

def refactor_css():
    with open('landing-page/style.css', 'r') as f:
        css = f.read()

    # Replace root variables
    css = re.sub(r'--bg-color:.*?;', '--bg-color: #E2E8F0;', css)
    css = re.sub(r'--text-main:.*?;', '--text-main: #1E293B;', css)
    css = re.sub(r'--text-muted:.*?;', '--text-muted: #64748B;', css)
    css = re.sub(r'--primary:.*?;', '--primary: #0D9488;', css)
    css = re.sub(r'--primary-hover:.*?;', '--primary-hover: #0F766E;', css)
    css = re.sub(r'--accent-1:.*?;', '--accent-1: #14B8A6;', css)
    css = re.sub(r'--accent-2:.*?;', '--accent-2: #2DD4BF;', css)
    css = re.sub(r'--accent-3:.*?;', '--accent-3: #5EEAD4;', css)
    css = re.sub(r'--glass-bg:.*?;', '--glass-bg: #E2E8F0;', css)
    css = re.sub(r'--glass-border:.*?;', '--glass-border: transparent;', css)

    # Convert glassmorphism blurs and borders to claymorphism shadows
    css = css.replace('backdrop-filter: blur(16px);', '/* backdrop removed for clay */')
    css = css.replace('-webkit-backdrop-filter: blur(16px);', '/* removed for clay */')
    css = css.replace('border: 1px solid var(--glass-border);', 'border: none;')
    
    # Generic glass card base
    css = re.sub(r'\.glass-card\s*\{[^}]*\}', 
    '''.glass-card {
  background: var(--bg-color);
  border-radius: 24px;
  border: none;
  box-shadow: 12px 12px 24px #cbd5e1, -12px -12px 24px #ffffff;
  padding: 2rem;
  transition: transform 0.5s ease;
}''', css)

    # Hover glass card
    css = re.sub(r'\.glass-card:hover\s*\{[^}]*\}',
    '''.glass-card:hover {
  transform: translateY(-5px);
  box-shadow: 16px 16px 32px #cbd5e1, -16px -16px 32px #ffffff;
}''', css)

    # Buttons (Primary)
    css = css.replace(
        'background: linear-gradient(135deg, var(--primary), var(--accent-2));',
        'background: var(--primary); box-shadow: 6px 6px 12px #cbd5e1, -6px -6px 12px #ffffff, inset 2px 2px 4px rgba(255,255,255,0.3);'
    )
    css = css.replace(
        'box-shadow: 0 4px 14px 0 rgba(79, 70, 229, 0.39);',
        ''
    )
    css = css.replace(
        'box-shadow: 0 6px 20px rgba(79, 70, 229, 0.5);',
        'box-shadow: 8px 8px 16px #cbd5e1, -8px -8px 16px #ffffff, inset 2px 2px 4px rgba(255,255,255,0.3);'
    )

    # Inputs
    css = re.sub(r'\.input-field\s*\{[^}]*\}',
    '''.input-field {
  flex: 1; padding: 0.875rem 1.5rem; border-radius: 9999px;
  background: var(--bg-color); border: none; color: var(--text-main); font-size: 1rem;
  font-family: var(--font-main); transition: all 0.3s ease;
  box-shadow: inset 6px 6px 12px #cbd5e1, inset -6px -6px 12px #ffffff;
}''', css)

    css = re.sub(r'\.input-field:focus\s*\{[^}]*\}',
    '''.input-field:focus {
  outline: none;
  box-shadow: inset 8px 8px 16px #cbd5e1, inset -8px -8px 16px #ffffff, 0 0 0 2px rgba(13, 148, 136, 0.3);
}''', css)

    # Replace specific colors
    css = css.replace('var(--text-main)', '#1E293B')
    css = css.replace('var(--text-muted)', '#64748B')
    css = css.replace('.bg-purple', '.bg-teal')
    
    # Let's write back
    with open('landing-page/style.css', 'w') as f:
        f.write(css)

if __name__ == "__main__":
    refactor_css()
    print("style.css Claymorphism patch complete!")
