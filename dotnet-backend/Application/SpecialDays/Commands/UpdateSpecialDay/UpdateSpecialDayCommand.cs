using Application.SpecialDays.Models;
using Domain.Entities;
using MediatR;
using Microsoft.EntityFrameworkCore;
using Persistence;

namespace Application.SpecialDays.Commands.UpdateSpecialDay;
public class UpdateSpecialDayCommand : SpecialDayRequestModel, IRequest<SpecialDay>
{
    public Guid Id { get; set; }
}

public class UpdateSpecialDayCommandHandler(ApplicationDbContext context) : IRequestHandler<UpdateSpecialDayCommand, SpecialDay>
{
    public async Task<SpecialDay> Handle(UpdateSpecialDayCommand request, CancellationToken cancellationToken)
    {
        var entity = await context.Set<SpecialDay>().FirstOrDefaultAsync(x => x.Id == request.Id, cancellationToken: cancellationToken);
        if (entity == null)
        {
            throw new KeyNotFoundException($"SpecialDay with Id {request.Id} not found.");
        }

        entity.Name = request.Name;
        entity.Date = request.Date;
        entity.Description = request.Description;

        await context.SaveChangesAsync(cancellationToken);
        return entity;
    }
}
