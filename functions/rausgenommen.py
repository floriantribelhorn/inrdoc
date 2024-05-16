                if alles:
                    nichtgewählte = [key for key, checked in checked_boxes.items() if not checked]
                    st.success(nichtgewählte)
                    for state in nichtgewählte:
                        st.session_state[f'{state}'] = True
                        st.write(st.session_state[f'{state}'])