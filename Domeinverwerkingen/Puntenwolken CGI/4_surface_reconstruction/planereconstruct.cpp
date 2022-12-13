#include <CGAL/Exact_predicates_inexact_constructions_kernel.h>
#include <CGAL/IO/read_ply_points.h>
#include <CGAL/IO/OBJ.h>
#include <CGAL/property_map.h>
#include <CGAL/Surface_mesh.h>
#include <CGAL/Shape_detection/Efficient_RANSAC.h>
#include <CGAL/Polygonal_surface_reconstruction.h>
#ifdef CGAL_USE_SCIP
#define SCIP_DEBUG
#include <CGAL/SCIP_mixed_integer_program_traits.h>
typedef CGAL::SCIP_mixed_integer_program_traits<double> MIP_Solver;
#elif defined(CGAL_USE_GLPK)
#include <CGAL/GLPK_mixed_integer_program_traits.h>
typedef CGAL::GLPK_mixed_integer_program_traits<double> MIP_Solver;
#endif
#if defined(CGAL_USE_GLPK) || defined(CGAL_USE_SCIP)
#include <CGAL/Timer.h>
#include <fstream>
#include <iostream>

#define MIN_PARAMETERS 7

typedef CGAL::Exact_predicates_inexact_constructions_kernel Kernel;
typedef Kernel::Point_3 Point;
typedef Kernel::Vector_3 Vector;
// Point with normal, and plane index
typedef boost::tuple<Point, Vector, int> PNI;
typedef std::vector<PNI> Point_vector;
typedef CGAL::Nth_of_tuple_property_map<0, PNI> Point_map;
typedef CGAL::Nth_of_tuple_property_map<1, PNI> Normal_map;
typedef CGAL::Nth_of_tuple_property_map<2, PNI> Plane_index_map;
typedef CGAL::Shape_detection::Efficient_RANSAC_traits<Kernel, Point_vector, Point_map, Normal_map> Traits;
typedef CGAL::Shape_detection::Efficient_RANSAC<Traits> Efficient_ransac;
typedef CGAL::Shape_detection::Plane<Traits> Plane;
typedef CGAL::Shape_detection::Point_to_shape_index_map<Traits> Point_to_shape_index_map;
typedef CGAL::Polygonal_surface_reconstruction<Kernel> Polygonal_surface_reconstruction;
typedef CGAL::Surface_mesh<Point> Surface_mesh;


int main(int argc, char *argv[])
{
        if (argc < MIN_PARAMETERS)
        {
                std::cout << "no valid input found" << std::endl;
                return (-1);
        }
        std::string input_file_name = argv[1];
        std::string outputpath = argv[2];
        std::string output_file_name = argv[3];
        float fitting = std::stof(argv[4]);
        float coverage = std::stof(argv[5]);
        float complexity = std::stof(argv[6]);
        if ((fitting + coverage + complexity) >  1.0f) {
                std::cout << fitting << " " << coverage << " " << complexity << std::endl;
                std::cerr << "Parameters sum to greater than 1" << std::endl;
                return EXIT_FAILURE; 
        };

        Point_vector points;
        const std::string input_file(input_file_name);
        std::ifstream input_stream(input_file.c_str(), std::ios::binary);
        if (input_stream.fail())
        {
                std::cerr << "failed open file \'" << input_file << "\'" << std::endl;
                return EXIT_FAILURE;
        }
        std::cout << "Loading point cloud: " << input_file << "...";
        CGAL::Timer t;
        t.start();
        if (!input_stream ||
            !CGAL::read_ply_points_with_properties(input_stream,
                                                   std::back_inserter(points),
                                                   CGAL::make_ply_point_reader(Point_map()),
                                                   CGAL::make_ply_normal_reader(Normal_map())))

        {
                std::cerr << "Error: cannot read file " << input_file << std::endl;
                return EXIT_FAILURE;
        }
        else
                std::cout << " Done. " << points.size() << " points. Time: " << t.time() << " sec." << std::endl;

        Efficient_ransac ransac;
        ransac.set_input(points);
        ransac.add_shape_factory<Plane>();

        Efficient_ransac::Parameters parameters;
        parameters.probability = 0.05;
        parameters.min_points = 200;
        parameters.epsilon = 0.1;
        parameters.cluster_epsilon = 0.1;
        parameters.normal_threshold = 0.9;

        std::cout << "Extracting planes...";
        t.reset();
        ransac.detect(parameters);
        Efficient_ransac::Plane_range planes = ransac.planes();
        std::size_t num_planes = planes.size();
        std::cout << " Done. " << num_planes << " planes extracted. Time: " << t.time() << " sec." << std::endl;
        // Stores the plane index of each point as the third element of the tuple.
        Point_to_shape_index_map shape_index_map(points, planes);
        for (std::size_t i = 0; i < points.size(); ++i)
        {
                // Uses the get function from the property map that accesses the 3rd element of the tuple.
                int plane_index = get(shape_index_map, i);
                points[i].get<2>() = plane_index;
        }
        std::cout << "Generating candidate faces...";
        t.reset();
        Polygonal_surface_reconstruction algo(
            points,
            Point_map(),
            Normal_map(),
            Plane_index_map());
        std::cout << " Done. Time: " << t.time() << " sec." << std::endl;
        Surface_mesh model;
        std::cout << "Reconstructing..." << std::endl;
        t.reset();
        // Fitting, Coverage, Complexity weights 
        if (!algo.reconstruct<MIP_Solver>(model, fitting, coverage, complexity))
        {
                std::cerr << " Failed: " << algo.error_message() << std::endl;
                return EXIT_FAILURE;
        }
        std::cout << "Done reconstructing with no errormessages" << std::endl;

        const std::string &output_file(outputpath + "/" + output_file_name +"_result.obj");
        std::ofstream output_stream(output_file.c_str());
        if (output_stream && CGAL::IO::write_OBJ(output_stream, model))
                std::cout << " Done. Saved to " << output_file << ". Time: " << t.time() << " sec." << std::endl;
        else
        {
                std::cerr << " Failed saving file." << std::endl;
                return EXIT_FAILURE;
        }
}
#else
int main(int, char **)
{
        std::cerr << "This program requires either GLPK or SCIP.\n";
        return EXIT_SUCCESS;
}
#endif // defined(CGAL_USE_GLPK) || defined(CGAL_USE_SCIP)

