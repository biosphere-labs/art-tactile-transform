import vtk

def main():
    # Create a reader
    reader = vtk.vtkSTLReader()
    reader.SetFileName("output.stl")

    # Create a mapper
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(reader.GetOutputPort())

    # Create an actor
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    # Create a renderer
    renderer = vtk.vtkRenderer()
    renderer.AddActor(actor)
    renderer.SetBackground(0.1, 0.2, 0.4)  # Dark blue background

    # Create a render window
    window = vtk.vtkRenderWindow()
    window.AddRenderer(renderer)

    # Create an interactor
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(window)

    # Initialize and start
    interactor.Initialize()
    window.Render()
    interactor.Start()

if __name__ == "__main__":
    main()