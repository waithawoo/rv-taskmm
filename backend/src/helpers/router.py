"""router.py

Provides helper functions for class based routing based on APIRouter

DON'T touch this module unless you don't know what you are doing.
"""

from functools import wraps
import inspect
from fastapi import APIRouter, Depends, HTTPException
from typing import Optional, Union


def route_method(methods: list, route_path: Union[str, list] = None, response_model=None, responses = None, dependencies: list = []):
    """
    Custom Decorator function to specify route methods for class based route register approach
    """

    def decorator(func):
        func.methods = methods
        func.route_path = route_path
        func.response_model = response_model
        func.responses = responses
        func.dependencies = dependencies
        return func

    return decorator


def register_routers(router: APIRouter, instance):
    """
    Registers routes dynamically based on methods defined in the instance.
        This method does the way _eg_register_routers() dynamically.
        e.g.
            def _eg_register_routers(self):
                self.router.add_api_route('/list', self.list, response_model=List[UserResponseModel], methods=['GET'])
                self.router.add_api_route('/signup', self.signup, methods=['POST'])
                self.router.add_api_route('/login', self.login, methods=['POST'])
    """
    for name, cls_method in inspect.getmembers(instance, predicate=inspect.ismethod):
        if name.startswith('_'):
            continue
        if getattr(cls_method, 'route_path') == '/':
            route_path = ''
        else:
            route_path = getattr(cls_method, 'route_path', None) or f'/{name.lower()}'
        methods = getattr(cls_method, 'methods', ['GET'])
        response_model = getattr(cls_method, 'response_model', None)
        responses = getattr(cls_method, 'responses', None)
        dependencies = getattr(cls_method, 'dependencies', [])

        if isinstance(route_path, list):
            for each_route_path in route_path:
                router.add_api_route(
                    path=each_route_path, 
                    endpoint=cls_method, 
                    response_model=response_model, 
                    methods=methods, 
                    responses=responses,
                    dependencies=dependencies,
                )
        else:
            router.add_api_route(
                path=route_path, 
                endpoint=cls_method, 
                response_model=response_model, 
                methods=methods, 
                responses=responses,
                dependencies=dependencies,
            )


# --- Set dependencies as middlewares

def _set_middleware_2_route(router: APIRouter, search: Union[str, None], middleware_dependency: Depends, by_name: bool = False, by_methods: Optional[list] = None):
    """
    Set various dependency middlewares to the specific route.
    
    Parameters:
    - router: The APIRouter containing the routes.
    - search: The path or name to search for.
    - middleware_dependency: The dependency middleware to be set
    - by_name: If True, search by route name, otherwise by path.
    
    Raise: HTTPException
    """
    from fastapi.params import Depends as DependsClass

    if not isinstance(middleware_dependency, DependsClass):
        middleware_dependency = Depends(middleware_dependency)

    route_found = False
    route_name = None
    # print('router ', router)
    # print('router ', router.routes[0].methods)
    
    for route in router.routes:
        route_name = route.path
        route_methods = route.methods
        if search == '*':
            route_found = True
            route.dependencies.append(middleware_dependency)
        else:
            if by_name and route.name == search:
                route_found = True
                route.dependencies.append(middleware_dependency)
            elif by_name and by_methods and route.path == search and any(method in route.methods for method in by_methods):
                route_found = True
                route.dependencies.append(middleware_dependency)
            elif not by_name and route.path == search:
                route_found = True
                route.dependencies.append(middleware_dependency)
    
    if not route_found:
        raise HTTPException(status_code=404, detail=f'{route_name} - Route not found')
    

def register_route_middlewares(routes: list[dict]):
    for route in routes:
        if len(route['middlewares']) > 0:
            for dependency, paths  in route['middlewares']:
                if paths[0] == '*':
                        _set_middleware_2_route(route['router'], '*', dependency)
                else:
                    for path in paths:
                        # print('path ', path)
                        if isinstance(path, tuple):
                            _set_middleware_2_route(route['router'], path[0], dependency, True, by_methods=[path[1]])
                        else:
                            _set_middleware_2_route(route['router'], path, dependency)


# --- Set response model as middlewares [NO longer used]

def _set_response_model_2_route(router: APIRouter, search: Union[str, None], res_model: None, by_name: bool = False):
    route_found = False
    for route in router.routes:
        if search == '*':
            route_found = True
            route.response_model = res_model
        else:
            if by_name and route.name == search:
                route_found = True
                route.response_model = res_model
            elif not by_name and route.path == search:
                route_found = True
                route.response_model = res_model
    
    if not route_found:
        raise HTTPException(status_code=404, detail='Route not found')
    

def register_route_res_model(routes: list[dict]):
    for route in routes:
        if len(route['response_models']) > 0:
            for res_model, paths  in route['response_models']:
                if paths[0] == '*':
                        _set_response_model_2_route(route['router'], '*', res_model)
                else:
                    for path in paths:
                        _set_response_model_2_route(route['router'], path, res_model)
