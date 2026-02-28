#%%
import FreeCAD as App
from app.optimize import run_optimization

def main():
    # Clean up any open documents
    for doc_name in App.listDocuments().keys():
        App.closeDocument(doc_name)

    # Run the optimization
    run_optimization()

if __name__ == "__main__":
    main()

# %%
