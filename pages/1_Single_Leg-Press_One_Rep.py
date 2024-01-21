import streamlit as st
import base64
import textwrap
from streamlit_dimensions import st_dimensions
from streamlit.elements.utils import _shown_default_value_warning
_shown_default_value_warning = True

def calc_single_leg_one_rep(weight, lift):
    if weight == 0:
        return lift
    else:
        return lift / weight


def update_weight_slider():
    st.session_state.weight_slider = st.session_state.weight_numeric

def update_weight_numeric():
    st.session_state.weight_numeric = st.session_state.weight_slider

def update_lift_slider():
    st.session_state.lift_slider = st.session_state.lift_numeric

def update_lift_numeric():
    st.session_state.lift_numeric = st.session_state.lift_slider

def render_svg(svg):
    """Renders the given svg string."""
    b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
    html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64
    st.write(html, unsafe_allow_html=True)

def display_performance(percent):
    """ Performance is defined as
        red: 0 - 40%
        orange: 40 - 60%
        green: 60 - 150%
     """
    width = 0
    dim = st_dimensions()
    if dim:
        width = dim['width']
   
    # here total width is 150%
    end_red = int((40/150)*width)
    end_orange = int((60/150)*width)

    position = int((percent/150)*width)

    height_a = 40
    height_l = 20
    height_s = 10

    svg = f"""
        <svg width="{width}" height="{height_a}" xmlns="http://www.w3.org/2000/svg">
            <line x1="0" y1="{height_l}" x2="{end_red}" y2="{height_l}" stroke="red" 
                stroke-width="{height_s}" />
            <line x1="{end_red}" y1="{height_l}" x2="{end_orange}" y2="{height_l}" stroke="orange" 
                stroke-width="{height_s}" />
            <line x1="{end_orange}" y1="{height_l}" x2="{width}" y2="{height_l}" stroke="green" 
                stroke-width="{height_s}" />
            <!-- circle cx="{position}" cy="{height_l}" r="5" fill="white" / -->
            <svg x="{position-12}" >
              <path d="M17.5431 14.2672C17.8288 13.9673 17.8172 13.4926 17.5172 13.2069C17.2173 12.9212 16.7426 
              12.9328 16.4569 13.2328L17.5431 14.2672ZM11.4569 18.4828C11.1712 18.7827 11.1828 19.2574 11.4828 
              19.5431C11.7827 19.8288 12.2574 19.8172 12.5431 19.5172L11.4569 18.4828ZM11.4569 19.5172C11.7426 
              19.8172 12.2173 19.8288 12.5172 19.5431C12.8172 19.2574 12.8288 18.7827 12.5431 18.4828L11.4569 
              19.5172ZM7.5431 13.2328C7.25744 12.9328 6.78271 12.9212 6.48276 13.2069C6.18281 13.4926 6.17123 
              13.9673 6.4569 14.2672L7.5431 13.2328ZM11.25 19C11.25 19.4142 11.5858 19.75 12 19.75C12.4142 19.75 
              12.75 19.4142 12.75 19H11.25ZM12.75 5C12.75 4.58579 12.4142 4.25 12 4.25C11.5858 4.25 11.25 4.58579 
              11.25 5H12.75ZM16.4569 13.2328L11.4569 18.4828L12.5431 19.5172L17.5431 14.2672L16.4569 13.2328ZM12.5431 
              18.4828L7.5431 13.2328L6.4569 14.2672L11.4569 19.5172L12.5431 18.4828ZM12.75 19V5H11.25V19H12.75Z" 
              fill="#000000"/>
            </svg>
        </svg>
    """
    # st.write('## Rendering an SVG in Streamlit')
    # st.write('### SVG Input')
    # st.code(textwrap.dedent(svg), 'svg')

    st.write('### Performance Evaluation')
    render_svg(svg)

# Streamlit App
def main():
    st.title("Single Leg-Press One Repetition")

    #"st.session_state object:", st.session_state

    min_w = 0
    max_w = 200
    min_l = 0
    max_l = max_w

    cols = st.columns([2, 1, 2])
    weight = cols[0].number_input("Weight", key="weight_numeric", min_value=min_w, max_value=max_w, step=5,
                                  on_change=update_weight_slider)
    lift = cols[2].number_input("Lift", key="lift_numeric", min_value=min_l, max_value=max_l, step=5,
                                  on_change=update_lift_slider)

    st.slider("Weight", key="weight_slider", min_value=min_w, max_value=max_w, value=weight,
                                on_change=update_weight_numeric)
    st.slider("Lift", key="lift_slider", min_value=min_l, max_value=max_l, value=lift,
                                  on_change=update_lift_numeric)

    # Percentage of lift to weight
    lift_percentage = calc_single_leg_one_rep(weight, lift)
    percent = int(lift_percentage * 100)
    display_performance(percent)
    st.write()
    st.text("The lift percentage to weight is: " + str(percent) + "%")


if __name__ == "__main__":
    main()
