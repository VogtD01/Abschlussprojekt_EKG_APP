import streamlit as st

def seite5():
    st.markdown("<h1 style='color:White;'>Impressum</h1>", unsafe_allow_html=True)
    
    st.markdown("<h3 style='color:White;'>Verantwortlich für den Inhalt</h3>", unsafe_allow_html=True)
    
    st.markdown("<p style='color:White;'><strong>Dominic Vogt</strong></p>", unsafe_allow_html=True)
    st.markdown("<p style='color:White;'>Geboren: 2001</p>", unsafe_allow_html=True)
    st.markdown("<p style='color:White;'>Studium: Medizin, Gesundheits- und Sporttechnologie</p>", unsafe_allow_html=True)
    st.markdown("<p style='color:White;'>Hochschule: Management Center Innsbruck (MCI), Innsbruck, Österreich</p>", unsafe_allow_html=True)
    
    st.write("---")
    
    st.markdown("<p style='color:White;'><strong>Felix Sturm</strong></p>", unsafe_allow_html=True)
    st.markdown("<p style='color:White;'>Geboren: 2004</p>", unsafe_allow_html=True)
    st.markdown("<p style='color:White;'>Studium: Medizin, Gesundheits- und Sporttechnologie</p>", unsafe_allow_html=True)
    st.markdown("<p style='color:White;'>Hochschule: Management Center Innsbruck (MCI), Innsbruck, Österreich</p>", unsafe_allow_html=True)
    
    st.write("---")
    
    st.markdown("<h3 style='color:White;'>Kontakt</h3>", unsafe_allow_html=True)
    
    st.markdown("<p style='color:White;'>E-Mail: dominic@vogt-schaer.de</p>", unsafe_allow_html=True)
    
    st.write("---")
    
    st.markdown("<h3 style='color:White;'>Hinweis zur Richtigkeit der Inhalte</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color:White;'>Der Inhalt dieser Webseite wurde nach bestem Wissen erstellt. Dennoch können wir keine Gewähr für die Richtigkeit, Vollständigkeit und Aktualität der bereitgestellten Inhalte übernehmen.</p>", unsafe_allow_html=True)
    
    st.write("---")
    
    
    st.markdown("<h3 style='color:White;'>Urheberrecht</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color:White;'>Die Inhalte und Werke auf dieser Webseite unterliegen dem österreichischen Urheberrecht. Die Vervielfältigung, Bearbeitung, Verbreitung und jede Art der Verwertung außerhalb der Grenzen des Urheberrechts bedürfen der schriftlichen Zustimmung des jeweiligen Autors bzw. Erstellers.</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    seite5()
