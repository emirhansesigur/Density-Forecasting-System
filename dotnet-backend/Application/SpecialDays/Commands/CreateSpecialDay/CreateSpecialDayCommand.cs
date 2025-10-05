using Application.SpecialDays.Models;
using Domain.Entities;
using MediatR;
using Persistence;

namespace Application.SpecialDays.Commands.CreateSpecialDay;
public class CreateSpecialDayCommand : SpecialDayRequestModel, IRequest<SpecialDay>
{
}

public class CreateSpecialDayCommandHandler(ApplicationDbContext context) : IRequestHandler<CreateSpecialDayCommand, SpecialDay>
{
    public async Task<SpecialDay> Handle(CreateSpecialDayCommand request, CancellationToken cancellationToken)
    {
        var entity = new SpecialDay
        {
            Name = request.Name,
            Date = request.Date,
            Description = request.Description
        };

        await context.Set<SpecialDay>().AddAsync(entity, cancellationToken);
        await context.SaveChangesAsync(cancellationToken);
        return entity;
    }
}
